"""
WhitePages Vendor
"""
# Python
import logging
# 3rd Party
import requests
import simplejson as json
# * * *
from vendor import Vendor

log = logging.getLogger(__name__)

@Vendor.register(name="WhitePages")
class WhitePages(Vendor):
  
  def __init__(self, config):
    self.uri_base = "http://proapi.whitepages.com/2.1/phone.json?phone_number={number}&api_key={api_key}"
    self.api_key = config["api_key"]

  def lookup(self, number):
    """
    Perform a lookup

    Args:
      number (str): phone number to lookup

    Returns:
      LookupResult
    """

    response = requests.get(self.uri_base.format(number=number, api_key=self.api_key))

    if( response.status_code!=200 ):
      result = Vendor.LOOKUP_FAILED
    else:
      result = self._parse(response.text)

    return result
    
  def _parse(self, response):
    """
    Parse the response text

    Args:
      response (str): the response json string

    Returns:
      LookupResult namedtuple
    """

    log.debug("Parsing: {}".format(response))
    data = json.loads(response)

    contacts = []
    for result in data["results"]:
      # Determine the name using "belongs_to"
      firstname = None
      lastname = None
      found_location = False

      for entity in result["belongs_to"]:
        # Find the name
        if firstname is None and lastname is None:
          if entity["id"]["type"] == "Business":
            lastname = entity["name"]

          else:
            # Keep the name that has both first_name and last_name
            for name in entity["names"]:
              if "first_name" in name or "last_name" in name:
                firstname = name.get("first_name", None)
                lastname = name.get("last_name", None)
              if "first_name" in name and "last_name" in name:
                break

          # If we got a last name, stop looking
          if lastname is not None:
            break

        # If there is a best_address, use it
        if entity["best_location"] is not None:
          found_location = True
          location = entity["best_location"]
          contact = self._parse_contact(firstname, lastname, location)

      # If we got no first or last name, raise ValueError
      if firstname is None and lastname is None:
        raise ValueError("Unable to parse name from data. Is that ok?")
      
      # If we got no location, check result["best_location"]
      if found_location
      for location in result["associated_locations"]:
        contact = {
          "firstname": firstname,
          "lastname": lastname}

        contacts.append(contact)

    # Done parsing. Create the LookupResult.
    result = Vendor.LookupResult(
      success=True,
      contacts=contacts)

    return result

  def _parse_contact(self, firstname, lastname, location):
    contact = {
      "firstname": firstname,
      "lastname": lastname}

    # Address
    if location.get("apt_type", None) is not None:
      contact["address"] = "{} {} {}, {} {}".format(
        location["house"], location["stret_name"], location["street_type"],
        location["apt_type"], location["apt_number"])
    elif location.get("box_number", None) is not None:
      contact["address"] = "PO Box {}".format(location["box_number"])
    else:
      contact["address"] = "{} {} {}".format(location["house"], location["street_name"], location["street_type"])

    contact["address"] = None
    contact["city"] = location["city"]
    contact["state"] = location["state_code"]
    if location["zip4"] is None:
      contact["zip"] = location["postal_code"]
    else:
      contact["zip"] = "{}-{}".format(location["postal_code"], location["zip4"])
    contact["country"] = location["country_code"]

    # Geocoding
    contact["geocoded"] = True
    contact["formatted_addr"] = location["address"]
    contact["geo_accuracy"] = location["lat_long"]["accuracy"]
    contact["latitude"]  = location["lat_long"]["latitude"]
    contact["longitude"] = location["lat_long"]["longitude"]

    return contact
        
  @property
  def name(self):
    """
    Return a unique representation for the vendor
    """
    return self._name

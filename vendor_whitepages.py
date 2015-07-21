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
    
  def lookdown(self, name, addr):
    """
    Perform a lookup of a name and address

    Args:
      name (str): name to lookup
      addr (str): addr to lookup

    Returns:
      LookdownResult
    """

    raise NotImplementedError("WhitePages plugin cannot perform lookdown()")

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
      number_location = None
      entity_location = None

      for entity in result["belongs_to"]:
        # Parse the name
        if firstname is None or lastname is None:
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

        # Grab the location
        if entity.get("best_location", None):
          entity_location = entity["best_location"]

        # If we got everything, stop looking
        if firstname and lastname and entity_location:
          break

      # Get the number's best location
      number_location = result["best_location"]

      # Prefer entity_location over number_location
      if entity_location:
        contact = self._parse_contact(firstname, lastname, entity_location)
      elif number_location:
        contact = self._parse_contact(firstname, lastname, number_location)
      else:
        contact = {"firstname": firstname, "lastname": lastname}

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
    contact["address"] = location["standard_address_line1"] if len(location["standard_address_line1"]) > 0 else None
    contact["line2"]   = location["standard_address_line2"] if len(location["standard_address_line2"]) > 0 else None
    if contact["line2"] is None:
      del contact["line2"]

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

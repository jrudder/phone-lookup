"""
PacificEast Vendor
"""
# Python
import logging
# 3rd Party
import requests
from defusedxml import ElementTree
# * * *
from vendor import Vendor

log = logging.getLogger(__name__)

@Vendor.register(name="PacificEast")
class PacificEast(Vendor):

  def __init__(self, config):
    if config.get("account_id", None) is None:
      raise ValueError("PacificEast: account_id] must not be None")
    
    self.name = "PacificEast-{}".format("public" if config["public"] else "restricted")
    self.account_id = config["account_id"]
    if config["env"] == "dev":
      self.phone_uri = "https://clientdev.pacificeast.com/Services/Custom/2514/1_0/PECustomXML.svc"
      self.flexi_uri  = "https://clientdev.pacificeast.com/FlexiQuery/1_4/Flexiquery.svc"
    elif config["env"] == "prod":
      self.phone_uri = "https://secure.pacificeast.com/Services/Custom/2527/1_0/PECustomXML.svc"
      # self.flexi_uri  = None
    else:
      raise ValueError("PacificEast: env must be either 'dev' or 'prod'")


    self.public = config["public"]

  def lookup(self, number):
    """
    Perform a lookup

    Args:
      number (str): phone number to lookup

    Returns:
      LookupResult
    """

    xml = """<?xml version="1.0" encoding="utf-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cus="http://pacificeast.com/custom">
      <soapenv:Header/>
      <soapenv:Body>
        <cus:ReversePhoneLookup>
          <cus:accountID>{account_id}</cus:accountID>
          <cus:phoneNumber>{number}</cus:phoneNumber>
          <cus:queryType>{query_type}</cus:queryType>
        </cus:ReversePhoneLookup>
      </soapenv:Body>
    </soapenv:Envelope>
    """.format(
        account_id=self.account_id,
        query_type=("PublicOnly" if self.public else "RestrictedOnly"),
        number=number,
      )

    headers = {
      "Content-Type"  : "text/xml; charset=utf-8",
      "SOAPAction"    : "http://pacificeast.com/custom/ReversePhoneLookup"
    }

    response = requests.post(self.phone_uri, data=xml, headers=headers)

    log.debug(response.status_code)
    log.debug(response.text)
    print(response.text)
    
    if( response.status_code!=200 ):
      result = Vendor.LOOKUP_FAILED
    else:
      result = self._parse(response.text)

    return result

  def lookdown(self, address, city, state, postalCode, country):
    """
    Perform a lookup of a name and address

    Args:
      address (str): line1 and line2 of the address to lookup
      city (str): city of the address to lookup
      state (str): state of the address to lookup
      postalCode (str): five- or nine-digit postal code of the address to lookup
      country (str): two-character ISO country code

    Returns:
      LookdownResult
    """

    xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pac="http://pacificeast.com/">
        <soapenv:Header/>
        <soapenv:Body>
          <pac:GetResponse>
            <pac:accountID>{account_id}</pac:accountID>
            <pac:subscriber>CLI-DEMO</pac:subscriber>
            <pac:purpose>AD</pac:purpose>
            <pac:queryType>RAD</pac:queryType>
            <pac:address>{address}</pac:address>
            <pac:city>{city}</pac:city>
            <pac:state>{state}</pac:state>
            <pac:postal>{postalCode}</pac:postal>
            <pac:country>{country}</pac:country>
          </pac:GetResponse>
       </soapenv:Body>
    </soapenv:Envelope>
    """.format(
      account_id=self.account_id,
      address=address,
      city=city,
      state=state,
      postalCode=postalCode,
      country=country)

    headers = {
      "Content-Type"  : "text/xml; charset=utf-8",
      "SOAPAction"    : "http://pacificeast.com/IFlexiQuery/GetResponse"
    }

    response = requests.post(self.flexi_uri, data=xml, headers=headers)

    log.debug(response.status_code)
    log.debug(response.text)
    print(response.text)
    
    if( response.status_code!=200 ):
      result = Vendor.LOOKUP_FAILED
    else:
      result = self._parse_lookdown(response.text)

    return result

  def _parse(self, response):
    """
    Parse the response text

    Args:
      response (str): the response xml

    Returns:
      LookupResult namedtuple
    """

    try:
      xml = ElementTree.fromstring(response)
    except ElementTree.ParseError:
      log.error("Failed to parse xml", exc_info=True)
      print("Failed to parse xml")
      result = Vendor.LOOKUP_FAILED

    else:
      node = xml.find("{http://schemas.xmlsoap.org/soap/envelope/}Body/{http://pacificeast.com/custom}ReversePhoneLookupResponse/{http://pacificeast.com/custom}ReversePhoneLookupResult/{http://pacificeast.com/custom}ContactsFound")
      if node.text == "0":
        result = Vendor.LOOKUP_FAILED
      else:
        # Contacts
        contacts = []
        for e in xml.findall("{http://schemas.xmlsoap.org/soap/envelope/}Body/{http://pacificeast.com/custom}ReversePhoneLookupResponse/{http://pacificeast.com/custom}ReversePhoneLookupResult/{http://pacificeast.com/custom}Contacts/{http://pacificeast.com/custom}Contact"):
          contact = {}
          if e.find("{http://pacificeast.com/custom}FirstName") is not None: contact["firstname"] = e.find("{http://pacificeast.com/custom}FirstName").text
          if e.find("{http://pacificeast.com/custom}LastName") is not None: contact["lastname"] = e.find("{http://pacificeast.com/custom}LastName").text
          if e.find("{http://pacificeast.com/custom}Address") is not None: contact["address"] = e.find("{http://pacificeast.com/custom}Address").text
          if e.find("{http://pacificeast.com/custom}City") is not None: contact["city"] = e.find("{http://pacificeast.com/custom}City").text
          if e.find("{http://pacificeast.com/custom}State") is not None: contact["state"] = e.find("{http://pacificeast.com/custom}State").text
          if e.find("{http://pacificeast.com/custom}Postal") is not None: contact["zip"] = e.find("{http://pacificeast.com/custom}Postal").text
          if e.find("{http://pacificeast.com/custom}Country") is not None: contact["country"] = e.find("{http://pacificeast.com/custom}Country").text
          if e.find("{http://pacificeast.com/custom}StartDate") is not None: contact["startdate"] = e.find("{http://pacificeast.com/custom}StartDate").text
          contacts.append(contact)

        # Done parsing. Create the LookupResult.
        result = Vendor.LookupResult(
          success=True,
          contacts=contacts)

    return result

  def _parse_lookdown(self, response):
    """
    Parse the response text of a lookdown

    Args:
      response (str): the response xml

    Returns:
      LookupResult namedtuple
    """

    try:
      xml = ElementTree.fromstring(response)
    except ElementTree.ParseError:
      log.error("Failed to parse xml", exc_info=True)
      print("Failed to parse xml")
      result = Vendor.LOOKUP_FAILED

    else:
      # Contacts
      contacts = []

      # Parse listings into contacts
      for e in xml.findall(
        "{http://schemas.xmlsoap.org/soap/envelope/}Body" +
        "/{http://pacificeast.com/}GetResponseResponse" +
        "/{http://pacificeast.com/}GetResponseResult" +
        "/{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}ListingInfo" +
        "/{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}Listings" +
        "/{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}Listing"):

        # Create a contact for each listing
        contact = {}
        self._grab_xml_entry(contact, "firstname",  e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}FirstName")
        self._grab_xml_entry(contact, "lastname",   e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}LastName")
        self._grab_xml_entry(contact, "address",    e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}Address")
        self._grab_xml_entry(contact, "city",       e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}City")
        self._grab_xml_entry(contact, "state",      e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}State")
        self._grab_xml_entry(contact, "country",    e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}Country")
        self._grab_xml_entry(contact, "carrier",    e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}Carrier")
        self._grab_xml_entry(contact, "phone",      e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}Phone")
        self._grab_xml_entry(contact, "linetype",   e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}PhoneServiceType")
        self._grab_xml_entry(contact, "restricted", e, "{http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery}RestrictedData")
        if "restricted" in contact: contact["restricted"] = True if contact["restricted"].lower()=="true" else False
        if "linetype" in contact: contact["linetype"] = contact["linetype"].lower()
        contacts.append(contact)

      # Done parsing. Create the LookupResult.
      result = Vendor.LookupResult(
        success=True,
        contacts=contacts)

    return result

  def _grab_xml_entry(self, d, key, e, path):
    """
    Set the dictionary entry to e.find(path).text if e.find(path) is not None
    """
    node = e.find(path)
    if node is not None:
      d[key] = node.text

  def name(self):
    """
    Return a unique representation for the vendor
    """
    return self.name

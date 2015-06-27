"""
Mock Vendor
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
    self.name = "PacificEast-{}".format("public" if config["public"] else "restricted")
    self.account_id = config["account_id"]
    self.uri = "https://secure.pacificeast.com/Services/Custom/2527/1_0/PECustomXML.svc"
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

    response = requests.post(self.uri, data=xml, headers=headers)

    log.debug(response.status_code)
    log.debug(response.text)
    print(response.status_code)
    print(response.text)

    if( response.status_code!=200 ):
      result = Vendor.LOOKUP_FAILED
    else:
      result = self.__parse(response.text)

    return result

  def __parse(self, response):
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
    

  def name(self):
    """
    Return a unique representation for the vendor
    """
    return self.name

  def self_test(self):
    """
    Test yourself
    """

    self.test_1()
    self.test_2()

  def test_1(self):
    xml = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <ReversePhoneLookupResponse xmlns="http://pacificeast.com/custom">
        <ReversePhoneLookupResult>
          <QueryPhone>3105551234</QueryPhone>
          <PhoneServiceType>Unknown</PhoneServiceType>
          <ContactsFound>0</ContactsFound>
          </ReversePhoneLookupResult>
        </ReversePhoneLookupResponse>
      </s:Body>
    </s:Envelope>"""
    result = self.__parse(xml)
    assert result.success == False

  def test_2(self):
    xml = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <ReversePhoneLookupResponse xmlns="http://pacificeast.com/custom">
        <ReversePhoneLookupResult>
          <QueryPhone>3105551234</QueryPhone>
          <PhoneServiceType>Unknown</PhoneServiceType>
          <ContactsFound>2</ContactsFound>
          <Contacts>
            <Contact>
              <FirstName>Bob</FirstName>
              <LastName>Smith</LastName>
            </Contact>
            <Contact>
              <FirstName>Sally</FirstName>
              <LastName>Jones</LastName>
            </Contact>
          </Contacts>          
          </ReversePhoneLookupResult>
        </ReversePhoneLookupResponse>
      </s:Body>
    </s:Envelope>"""
    result = self.__parse(xml)
    assert result.success == True
    assert len(result.contacts) == 2
    assert result.contacts[0] == {"firstname": "Bob", "lastname": "Smith"}
    assert result.contacts[1] == {"firstname": "Sally", "lastname": "Jones"}


  

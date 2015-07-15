"""
Test the PacificEast vendor
"""

# Python
from unittest.mock import patch
# * * *
from vendor import Vendor
from vendor_pacificeast import PacificEast

def test_config():
  """ Ensure that the config is properly parsed """

  # Create an instance of the vendor
  s = Vendor.get("pacificeast", config={"public": True, "account_id": "1234"})

  with patch("vendor_pacificeast.requests.post") as mock_post:
    # Configure the mock object
    mock_post.result.status_code = 200
    mock_post.result.text = XML_NO_RESULT

    # Call lookup to ensure that the config passes properly to requests
    s.lookup("3105550000")
    assert mock_post.called
    assert mock_post.call_count == 1
    assert "<cus:accountID>1234</cus:accountID>" in mock_post.call_args[1]["data"]

def test_no_result():
  """ Handle response of no contacts found """
  s = Vendor.get("pacificeast", config={"public": True, "account_id": "1234"})
  lookup_result = s._parse(XML_NO_RESULT)
  assert lookup_result.success == False

def test_multiple_contacts():
  """ Handle response of multiple contacts found """
  s = Vendor.get("pacificeast", config={"public": True, "account_id": "1234"})
  lookup_result = s._parse(XML_MULTIPLE_CONTACTS)
  assert len(lookup_result.contacts) == 2
  assert lookup_result.contacts[0] == {"firstname": "Bob", "lastname": "Smith"}
  assert lookup_result.contacts[1] == {"firstname": "Sally", "lastname": "Jones"}


"""
XML Definitions
"""

XML_NO_RESULT = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
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

XML_MULTIPLE_CONTACTS = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
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
  
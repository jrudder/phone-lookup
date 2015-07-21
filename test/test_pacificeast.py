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
  s = Vendor.get("pacificeast", config={"public": True, "account_id": "1234", "env": "dev"})

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
  s = Vendor.get("pacificeast", config={"public": True, "account_id": "1234", "env": "dev"})
  lookup_result = s._parse(XML_NO_RESULT)
  assert lookup_result.success == False

def test_multiple_contacts():
  """ Handle response of multiple contacts found """
  s = Vendor.get("pacificeast", config={"public": True, "account_id": "1234", "env": "dev"})
  lookup_result = s._parse(XML_MULTIPLE_CONTACTS)
  assert len(lookup_result.contacts) == 2
  assert lookup_result.contacts[0] == {"firstname": "Bob", "lastname": "Smith"}
  assert lookup_result.contacts[1] == {"firstname": "Sally", "lastname": "Jones"}

def test_rad_result():
  """ Ensure that RAD result is parsed correctly """
  s = Vendor.get("pacificeast", config={"public": True, "account_id": "1234", "env": "dev"})
  lookdown_result = s._parse_lookdown(XML_RAD_RESULT)
  assert len(lookdown_result.contacts) == 3
  assert lookdown_result.contacts[0] == XML_RAD_RESULTS[0]
  assert lookdown_result.contacts[1] == XML_RAD_RESULTS[1]
  assert lookdown_result.contacts[2] == XML_RAD_RESULTS[2]

  """
  <a:CreationDate>20150601</a:CreationDate>
  <a:Latitude/>
  <a:ListingSource>DA</a:ListingSource>
  <a:ListingType>RS</a:ListingType>
  <a:Longitude/>
  <a:NonPublished>false</a:NonPublished>
  
  <a:Carrier>AT&amp;T</a:Carrier>
  <a:Phone>3105551236</a:Phone>
  <a:PhoneServiceType>Landline</a:PhoneServiceType>
  
  <a:Ported>N</a:Ported>
  <a:Postal>123459876</a:Postal>
  <a:RestrictedData>false</a:RestrictedData>
  <a:TransactionDate>20150601</a:TransactionDate>
  """

"""
XML Definitions
"""

XML_RAD_NO_RESULTS = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <GetResponseResponse xmlns="http://pacificeast.com/">
         <GetResponseResult xmlns:a="http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <a:ErrorInfo i:nil="true"/>
            <a:LineInfo i:nil="true"/>
            <a:ListingInfo i:nil="true"/>
            <a:QueryType>RAD</a:QueryType>
            <a:ReferenceID i:nil="true"/>
            <a:ResultCode>0</a:ResultCode>
            <a:SSNInfo i:nil="true"/>
            <a:StandardizationInfo i:nil="true"/>
            <a:VerificationInfo i:nil="true"/>
         </GetResponseResult>
      </GetResponseResponse>
   </s:Body>
</s:Envelope>"""

XML_RAD_RESULTS = [
  {
    "firstname": "Sally",
    "lastname": "Smith",
    "carrier": "AT&T",
    "phone": "3105551236",
    "linetype": "landline",
    "address": "123 Main St",
    "city": "Anytown",
    "state": "NY",
    "country": "US"},
  {
    "firstname": "Jane",
    "lastname": "Smith",
    "carrier": "AT&T",
    "phone": "3105551236",
    "linetype": "landline",
    "address": "123 Main St",
    "city": "Anytown",
    "state": "NY",
    "country": "US"},
  {
    "firstname": "Susan",
    "lastname": "Smith",
    "carrier": "AT&T",
    "phone": "3105551236",
    "linetype": "landline",
    "address": "123 Main St",
    "city": "Anytown",
    "state": "NY",
    "country": "US"},
]

XML_RAD_RESULT = """<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
   <s:Body>
      <GetResponseResponse xmlns="http://pacificeast.com/">
         <GetResponseResult xmlns:a="http://schemas.datacontract.org/2004/07/PE.RealTime.FlexiQuery" xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
            <a:ErrorInfo i:nil="true"/>
            <a:LineInfo i:nil="true"/>
            <a:ListingInfo>
               <a:Listings>
                  <a:Listing>
                     <a:Address>123 Main St</a:Address>
                     <a:BusinessName/>
                     <a:Carrier>AT&amp;T</a:Carrier>
                     <a:City>Anytown</a:City>
                     <a:Country>US</a:Country>
                     <a:CreationDate>20150601</a:CreationDate>
                     <a:FirstName>Sally</a:FirstName>
                     <a:LastName>Smith</a:LastName>
                     <a:Latitude/>
                     <a:ListingSource>DA</a:ListingSource>
                     <a:ListingType>RS</a:ListingType>
                     <a:Longitude/>
                     <a:NonPublished>false</a:NonPublished>
                     <a:Phone>3105551236</a:Phone>
                     <a:PhoneServiceType>Landline</a:PhoneServiceType>
                     <a:Ported>N</a:Ported>
                     <a:Postal>123459876</a:Postal>
                     <a:RestrictedData>false</a:RestrictedData>
                     <a:State>NY</a:State>
                     <a:TransactionDate>20150601</a:TransactionDate>
                  </a:Listing>
                  <a:Listing>
                     <a:Address>123 Main St</a:Address>
                     <a:BusinessName/>
                     <a:Carrier>AT&amp;T</a:Carrier>
                     <a:City>Anytown</a:City>
                     <a:Country>US</a:Country>
                     <a:CreationDate>20150601</a:CreationDate>
                     <a:FirstName>Jane</a:FirstName>
                     <a:LastName>Smith</a:LastName>
                     <a:Latitude/>
                     <a:ListingSource>DA</a:ListingSource>
                     <a:ListingType>RS</a:ListingType>
                     <a:Longitude/>
                     <a:NonPublished>false</a:NonPublished>
                     <a:Phone>3105551236</a:Phone>
                     <a:PhoneServiceType>Landline</a:PhoneServiceType>
                     <a:Ported>N</a:Ported>
                     <a:Postal>123459876</a:Postal>
                     <a:RestrictedData>false</a:RestrictedData>
                     <a:State>NY</a:State>
                     <a:TransactionDate>20150601</a:TransactionDate>
                  </a:Listing>
                  <a:Listing>
                     <a:Address>123 Main St</a:Address>
                     <a:BusinessName/>
                     <a:Carrier>AT&amp;T</a:Carrier>
                     <a:City>Anytown</a:City>
                     <a:Country>US</a:Country>
                     <a:CreationDate>20150601</a:CreationDate>
                     <a:FirstName>Susan</a:FirstName>
                     <a:LastName>Smith</a:LastName>
                     <a:Latitude/>
                     <a:ListingSource>DA</a:ListingSource>
                     <a:ListingType>RS</a:ListingType>
                     <a:Longitude/>
                     <a:NonPublished>false</a:NonPublished>
                     <a:Phone>3105551236</a:Phone>
                     <a:PhoneServiceType>Landline</a:PhoneServiceType>
                     <a:Ported>N</a:Ported>
                     <a:Postal>123459876</a:Postal>
                     <a:RestrictedData>false</a:RestrictedData>
                     <a:State>NY</a:State>
                     <a:TransactionDate>20150601</a:TransactionDate>
                  </a:Listing>
               </a:Listings>
               <a:ListingsFound>3</a:ListingsFound>
            </a:ListingInfo>
            <a:QueryType>RAD</a:QueryType>
            <a:ReferenceID i:nil="true"/>
            <a:ResultCode>1</a:ResultCode>
            <a:SSNInfo i:nil="true"/>
            <a:StandardizationInfo i:nil="true"/>
            <a:VerificationInfo i:nil="true"/>
         </GetResponseResult>
      </GetResponseResponse>
   </s:Body>
</s:Envelope>"""

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
  
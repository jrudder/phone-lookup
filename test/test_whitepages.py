"""
Test the PacificEast vendor
"""

# Python
from unittest.mock import patch
import logging
# * * *
from vendor import Vendor
from vendor_whitepages import WhitePages

log = logging.getLogger(__name__)

def test_contact_found():
  """ Handle response of contact found """
  s = Vendor.get("WhitePages", config={"api_key": "1234"})
  lookup_result = s._parse(JSON_GOOD)
  assert lookup_result.success == True
  assert len(lookup_result.contacts) == 1
  assert lookup_result.contacts[0] == {
    "firstname": None, "lastname": "Whitepages",
    "formatted_addr": "Seattle WA 98115",
    "address": None,
    "city": "Seattle",
    "state": "WA",
    "country": "US",
    "zip": "98115",
    "geocoded": True,
    "geo_accuracy": "PostalCode",
    "latitude": 47.6851,
    "longitude": -122.2926
  }

def test_no_name():
  """ Handle response of address but no name """
  s = Vendor.get("WhitePages", config={"api_key": "1234"})
  lookup_result = s._parse(JSON_NO_NAME)
  assert lookup_result.success == True
  assert len(lookup_result.contacts) == 1
  assert lookup_result.contacts[0] == {
    "firstname": None, "lastname": None,
    "formatted_addr": "Mineola NY 11501",
    "address": None,
    "city": "Mineola",
    "state": "NY",
    "country": "US",
    "zip": "11501",
    "geocoded": True,
    "geo_accuracy": "PostalCode",
    "latitude": 40.7469,
    "longitude": -73.6388
  }

def test_best_location():
  """ Handle response of address but no name """
  s = Vendor.get("WhitePages", config={"api_key": "1234"})
  lookup_result = s._parse(JSON_BEST_LOCATION)
  assert lookup_result.success == True
  assert len(lookup_result.contacts) == 1
  log.debug(lookup_result.contacts)
  assert lookup_result.contacts[0] == {
    "firstname": "Bob", "lastname": "Bobson",
    "formatted_addr": "3434 Bubble Ct, Anytown CA 01234-4444",
    "address": "3434 Bubble Ct",
    "city": "Anytown",
    "state": "CA",
    "country": "US",
    "zip": "01234-4444",
    "geocoded": True,
    "geo_accuracy": "RoofTop",
    "latitude":24.688217,
    "longitude":-106.167145,
  }

def xtest_multiple_contacts():
  """ Handle response of multiple contacts found """
  s = Vendor.get("WhitePages", config={"api_key": "1234"})
  lookup_result = s._parse(JSON_GOOD)
  assert len(lookup_result.contacts) == 2
  assert lookup_result.contacts[0] == {"firstname": "Bob", "lastname": "Smith"}
  assert lookup_result.contacts[1] == {"firstname": "Sally", "lastname": "Jones"}


"""
JSON Definitions
"""


JSON_GOOD = """{
 "results":[
  {
   "id":{
    "key":"Phone.4d796fef-a2df-4b08-cfe3-bc7128b6f6bb.Durable",
    "url":"https://proapi.whitepages.com/2.1/entity/Phone.4d796fef-a2df-4b08-cfe3-bc7128b6f6bb.Durable.json?api_key=KEYVAL",
    "type":"Phone",
    "uuid":"4d796fef-a2df-4b08-cfe3-bc7128b6f6bb",
    "durability":"Durable"
   },
   "line_type":"Landline",
   "belongs_to":[
    {
     "id":{
      "key":"Business.ed5796c8-4e86-480a-b520-7a9f47f03a19.Durable",
      "url":"https://proapi.whitepages.com/2.1/entity/Business.ed5796c8-4e86-480a-b520-7a9f47f03a19.Durable.json?api_key=KEYVAL",
      "type":"Business",
      "uuid":"ed5796c8-4e86-480a-b520-7a9f47f03a19",
      "durability":"Durable"
     },
     "valid_for":null,
     "name":"Whitepages",
      "locations":[
      {
       "id":{
        "key":"Location.b4bad7f6-4095-4fbf-a997-130984ed94ad.Durable",
        "url":"https://proapi.whitepages.com/2.1/entity/Location.b4bad7f6-4095-4fbf-a997-130984ed94ad.Durable.json?api_key=KEYVAL",
        "type":"Location",
        "uuid":"b4bad7f6-4095-4fbf-a997-130984ed94ad",
        "durability":"Durable"
       },
       "contact_type":"Business",
       "type":"Address",
       "legal_entities_at":null,
       "city":"Palo Alto",
       "postal_code":"94306",
       "zip4":"2203",
       "state_code":"CA",
       "country_code":"US",
       "address":"411 Acacia Ave, Palo Alto, CA 94306-2203",
       "house":"411",
       "street_name":"Acacia",
       "street_type":"Ave",
       "apt_type":null,
       "is_receiving_mail":true,
       "not_receiving_mail_reason":null,
       "usage":null,
       "delivery_point":null,
       "box_type":null,
       "address_type":null,
       "lat_long":{
        "latitude":37.4225997924805,
        "longitude":-122.138076782227,
        "accuracy":"RoofTop"
       },
       "is_deliverable":true,
       "contained_by_locations":null
      }
     ],
     "phones":[
      {
       "id":{
        "key":"Phone.4d796fef-a2df-4b08-cfe3-bc7128b6f6bb.Durable",
        "url":"https://proapi.whitepages.com/2.1/entity/Phone.4d796fef-a2df-4b08-cfe3-bc7128b6f6bb.Durable.json?api_key=KEYVAL",
        "type":"Phone",
        "uuid":"4d796fef-a2df-4b08-cfe3-bc7128b6f6bb",
        "durability":"Durable"
       },
       "contact_type":"Business",
       "line_type":"Landline",
       "belongs_to":null,
       "associated_locations":null,
       "is_valid":true,
       "country_calling_code":"1",
       "extension":null,
       "carrier":"tw telecom",
       "do_not_call":false,
       "reputation":{
       "level":1,
       "details":[
         {
              "score": 10,
              "type": "not_spam"
          }
       ],
       "volume_score": 1,
       "report_count": 0
       },
       "is_prepaid":false,
       "best_location":null
      }
     ]
    },
    {
     "id":{
      "key":"Business.dfd13b90-b786-4f94-bfd3-b65d5a5cb088.Durable",
      "url":"https://proapi.whitepages.com/2.1/entity/Business.dfd13b90-b786-4f94-bfd3-b65d5a5cb088.Durable.json?api_key=KEYVAL",
      "type":"Business",
      "uuid":"dfd13b90-b786-4f94-bfd3-b65d5a5cb088",
      "durability":"Durable"
     },
     "valid_for":null,
     "name":"Whitepages",
     "locations":[
      {
       "id":{
        "key":"Location.a3c1ed9b-a709-4b58-a3bf-eb29727f6740.Ephemeral",
        "url":null,
        "type":"Location",
        "uuid":"a3c1ed9b-a709-4b58-a3bf-eb29727f6740",
        "durability":"Ephemeral"
       },
       "contact_type":null,
       "type":"Address",
       "legal_entities_at":null,
       "city":"New York",
       "postal_code":"10018",
       "zip4":null,
       "state_code":"NY",
       "country_code":null,
       "address":null,
       "house":null,
       "street_name":null,
       "street_type":null,
       "apt_type":null,
       "is_receiving_mail":null,
       "not_receiving_mail_reason":null,
       "usage":null,
       "delivery_point":null,
       "box_type":null,
       "address_type":null,
       "lat_long":{
        "latitude":40.753017,
        "longitude":-73.986237,
        "accuracy":null
       },
       "is_deliverable":null,
       "contained_by_locations":null
      }
     ],
     "phones":[
      {
       "id":{
        "key":"Phone.4d796fef-a2df-4b08-cfe3-bc7128b6f6bb.Durable",
        "url":"https://proapi.whitepages.com/2.1/entity/Phone.4d796fef-a2df-4b08-cfe3-bc7128b6f6bb.Durable.json?api_key=KEYVAL",
        "type":"Phone",
        "uuid":"4d796fef-a2df-4b08-cfe3-bc7128b6f6bb",
        "durability":"Durable"
       },
       "contact_type":"Business",
       "line_type":"Landline",
       "belongs_to":null,
       "associated_locations":null,
       "is_valid":true,
       "country_calling_code":"1",
       "extension":null,
       "carrier":"tw telecom",
       "do_not_call":false,
       "reputation":{
       "level":1,
       "details":[
         {
              "score": 10,
              "type": "not_spam"
          }
       ],
       "volume_score": 1,
       "report_count": 0
       },
       "is_prepaid":false,
       "best_location":null
      }
     ]
    },
    {
     "id":{
      "key":"Business.545ac847-02be-4f1c-8139-9e7b97b18003.Durable",
      "url":"https://proapi.whitepages.com/2.1/entity/Business.545ac847-02be-4f1c-8139-9e7b97b18003.Durable.json?api_key=KEYVAL",
      "type":"Business",
      "uuid":"545ac847-02be-4f1c-8139-9e7b97b18003",
      "durability":"Durable"
     },
     "valid_for":null,
     "name":"Whitepages",
     "locations":[
      {
       "id":{
        "key":"Location.f680d715-f932-4e68-9e64-9871113a6b81.Durable",
        "url":"https://proapi.whitepages.com/2.1/entity/Location.f680d715-f932-4e68-9e64-9871113a6b81.Durable.json?api_key=KEYVAL",
        "type":"Location",
        "uuid":"f680d715-f932-4e68-9e64-9871113a6b81",
        "durability":"Durable"
       },
       "contact_type":"Business",
       "type":"Address",
       "legal_entities_at":null,
       "city":"Seattle",
       "postal_code":"98101",
       "zip4":"2603",
       "state_code":"WA",
       "country_code":"US",
       "address":"1301 5th Ave, Seattle, WA 98101-2603",
       "house":"1301",
       "street_name":"5th",
       "street_type":"Ave",
       "apt_type":null,
       "is_receiving_mail":null,
       "not_receiving_mail_reason":null,
       "usage":null,
       "delivery_point":null,
       "box_type":null,
       "address_type":null,
       "lat_long":{
        "latitude":47.608624,
        "longitude":-122.334442,
        "accuracy":"RoofTop"
       },
       "is_deliverable":false,
       "contained_by_locations":null
      }
     ],
     "phones":[
      {
       "id":{
        "key":"Phone.4d796fef-a2df-4b08-cfe3-bc7128b6f6bb.Durable",
        "url":"https://proapi.whitepages.com/2.1/entity/Phone.4d796fef-a2df-4b08-cfe3-bc7128b6f6bb.Durable.json?api_key=KEYVAL",
        "type":"Phone",
        "uuid":"4d796fef-a2df-4b08-cfe3-bc7128b6f6bb",
        "durability":"Durable"
       },
       "contact_type":"Business",
       "line_type":"Landline",
       "belongs_to":null,
       "associated_locations":null,
       "is_valid":true,
       "country_calling_code":"1",
       "extension":null,
       "carrier":"tw telecom",
       "do_not_call":false,
       "reputation":{
       "level":1,
       "details":[
         {
              "score": 10,
              "type": "not_spam"
          }
       ],
       "volume_score": 1,
       "report_count": 0
       },
       "is_prepaid":false,
       "best_location":null
      },
      {
       "id":{
        "key":"Phone.345f6fef-a2e1-4b08-cfe3-bc7128b7ba13.Durable",
        "url":"https://proapi.whitepages.com/2.1/entity/Phone.345f6fef-a2e1-4b08-cfe3-bc7128b7ba13.Durable.json?api_key=KEYVAL",
        "type":"Phone",
        "uuid":"345f6fef-a2e1-4b08-cfe3-bc7128b7ba13",
        "durability":"Durable"
       },
       "contact_type":"Business",
       "line_type":"Landline",
       "belongs_to":null,
       "associated_locations":null,
       "is_valid":null,
       "country_calling_code":"1",
       "extension":null,
       "carrier":null,
       "do_not_call":null,
       "reputation":null,
       "is_prepaid":null,
       "best_location":null
      },
      {
       "id":{
        "key":"Phone.345f6fef-a2e1-4b08-cfe3-bc7128b7ba13.Durable",
        "url":"https://proapi.whitepages.com/2.1/entity/Phone.345f6fef-a2e1-4b08-cfe3-bc7128b7ba13.Durable.json?api_key=KEYVAL",
        "type":"Phone",
        "uuid":"345f6fef-a2e1-4b08-cfe3-bc7128b7ba13",
        "durability":"Durable"
       },
       "contact_type":"Business",
       "line_type":"Landline",
       "belongs_to":null,
       "associated_locations":null,
       "is_valid":null,
       "country_calling_code":"1",
       "extension":null,
       "carrier":null,
       "do_not_call":null,
       "reputation":null,
       "is_prepaid":null,
       "best_location":null
      }
     ]
    }
   ],
   "associated_locations":[
    {
     "id":{
      "key":"Location.31d25199-e4db-4b0b-a4e1-c463702f3eb6.Durable",
      "url":"https://proapi.whitepages.com/2.1/entity/Location.31d25199-e4db-4b0b-a4e1-c463702f3eb6.Durable.json?api_key=KEYVAL",
      "type":"Location",
      "uuid":"31d25199-e4db-4b0b-a4e1-c463702f3eb6",
      "durability":"Durable"
     },
     "contact_type":null,
     "type":"CityPostalCode",
     "legal_entities_at":null,
     "city":"Seattle",
     "postal_code":"98115",
     "zip4":null,
     "state_code":"WA",
     "country_code":"US",
     "address":"Seattle WA 98115",
     "house":null,
     "street_name":null,
     "street_type":null,
     "apt_type":null,
     "is_receiving_mail":null,
     "not_receiving_mail_reason":null,
     "usage":null,
     "delivery_point":null,
     "box_type":null,
     "address_type":null,
     "lat_long":{
      "latitude":47.6851,
      "longitude":-122.2926,
      "accuracy":"PostalCode"
     },
     "is_deliverable":null
    }
   ],
   "is_valid":true,
   "country_calling_code":"1",
   "extension":null,
   "carrier":"tw telecom",
   "do_not_call":false,
   "reputation":{
    "spam_score":6
   },
   "is_prepaid":false,
   "best_location":{
    "id":{
     "key":"Location.31d25199-e4db-4b0b-a4e1-c463702f3eb6.Durable",
     "url":"https://proapi.whitepages.com/2.1/entity/Location.31d25199-e4db-4b0b-a4e1-c463702f3eb6.Durable.json?api_key=KEYVAL",
     "type":"Location",
     "uuid":"31d25199-e4db-4b0b-a4e1-c463702f3eb6",
     "durability":"Durable"
    },
    "type":"CityPostalCode",
    "legal_entities_at":null,
    "city":"Seattle",
    "postal_code":"98115",
    "zip4":null,
    "state_code":"WA",
    "country_code":"US",
    "address":"Seattle WA 98115",
    "house":null,
    "street_name":null,
    "street_type":null,
    "apt_type":null,
    "is_receiving_mail":null,
    "not_receiving_mail_reason":null,
    "usage":null,
    "delivery_point":null,
    "box_type":null,
    "address_type":null,
    "lat_long":{
     "latitude":47.6851,
     "longitude":-122.2926,
     "accuracy":"PostalCode"
    },
    "is_deliverable":null,
    "standard_address_line1" :"",
    "standard_address_line2" :""
   }
  }
 ],
 "messages":[]
}"""

JSON_NO_NAME = """{
 "results":[
  {
   "id":{
    "key":"Phone.9fb36fef-a2e1-4b08-cfe3-bc7128b758c2.Durable",
    "url":"https://proapi.whitepages.com/2.1/entity/Phone.9fb36fef-a2e1-4b08-cfe3-bc7128b758c2.Durable.json?api_key=fa4bbd5febebc9849fe32bc80c6ee892",
    "type":"Phone",
    "uuid":"9fb36fef-a2e1-4b08-cfe3-bc7128b758c2",
    "durability":"Durable"
   },
   "line_type":"Mobile",
   "belongs_to":[],
   "associated_locations":[
    {
     "id":{
      "key":"Location.9c47a710-730c-42cd-9cfd-5f94da51afc8.Durable",
      "url":"https://proapi.whitepages.com/2.1/entity/Location.9c47a710-730c-42cd-9cfd-5f94da51afc8.Durable.json?api_key=fa4bbd5febebc9849fe32bc80c6ee892",
      "type":"Location",
      "uuid":"9c47a710-730c-42cd-9cfd-5f94da51afc8",
      "durability":"Durable"
     },
     "type":"CityPostalCode",
     "valid_for":null,
     "legal_entities_at":null,
     "city":"Mineola",
     "postal_code":"11501",
     "zip4":null,
     "state_code":"NY",
     "country_code":"US",
     "address":"Mineola NY 11501",
     "house":null,
     "street_name":null,
     "street_type":null,
     "pre_dir":null,
     "post_dir":null,
     "apt_number":null,
     "apt_type":null,
     "box_number":null,
     "is_receiving_mail":null,
     "not_receiving_mail_reason":null,
     "usage":null,
     "delivery_point":null,
     "box_type":null,
     "address_type":null,
     "lat_long":{
      "latitude":40.7469,
      "longitude":-73.6388,
      "accuracy":"PostalCode"
     },
     "is_deliverable":null,
     "standard_address_line1":"",
     "standard_address_line2":"",
     "standard_address_location":"Mineola NY 11501",
     "is_historical":false,
     "contact_type":null,
     "contact_creation_date":null
    }
   ],
   "is_valid":true,
   "country_calling_code":"1",
   "extension":null,
   "carrier":"Verizon Wireless",
   "do_not_call":true,
   "reputation":{
    "spam_score":2,
    "spam_index":1,
    "level":1,
    "details":[
     {
      "score":2,
      "type":"Uncertain",
      "category":"Unknown"
     }
    ]
   },
   "is_prepaid":null,
   "is_connected":true,
   "best_location":{
    "id":{
     "key":"Location.9c47a710-730c-42cd-9cfd-5f94da51afc8.Durable",
     "url":"https://proapi.whitepages.com/2.1/entity/Location.9c47a710-730c-42cd-9cfd-5f94da51afc8.Durable.json?api_key=fa4bbd5febebc9849fe32bc80c6ee892",
     "type":"Location",
     "uuid":"9c47a710-730c-42cd-9cfd-5f94da51afc8",
     "durability":"Durable"
    },
    "type":"CityPostalCode",
    "valid_for":null,
    "legal_entities_at":null,
    "city":"Mineola",
    "postal_code":"11501",
    "zip4":null,
    "state_code":"NY",
    "country_code":"US",
    "address":"Mineola NY 11501",
    "house":null,
    "street_name":null,
    "street_type":null,
    "pre_dir":null,
    "post_dir":null,
    "apt_number":null,
    "apt_type":null,
    "box_number":null,
    "is_receiving_mail":null,
    "not_receiving_mail_reason":null,
    "usage":null,
    "delivery_point":null,
    "box_type":null,
    "address_type":null,
    "lat_long":{
     "latitude":40.7469,
     "longitude":-73.6388,
     "accuracy":"PostalCode"
    },
    "is_deliverable":null,
    "standard_address_line1":"",
    "standard_address_line2":"",
    "standard_address_location":"Mineola NY 11501"
   }
  }
 ],
 "messages":[]
}"""

JSON_BEST_LOCATION = """{
 "results":[
  {
   "id":{
    "key":"Phone.ec7f6fef-a2e2-4b08-cfe3-bc7128b46deb.Durable",
    "url":"https://proapi.whitepages.com/2.1/entity/Phone.ec7f6fef-a2e2-4b08-cfe3-bc7128b46deb.Durable.json?api_key=fa4bbd5febebc9849fe32bc80c6ee892",
    "type":"Phone",
    "uuid":"ec7f6fef-a2e2-4b08-cfe3-bc7128b46deb",
    "durability":"Durable"
   },
   "line_type":"Mobile",
   "belongs_to":[
    {
     "id":{
      "key":"Person.f30752f6-9446-4bf5-872f-d57b1e0814f5.Ephemeral",
      "url":null,
      "type":"Person",
      "uuid":"f30752f6-9446-4bf5-872f-d57b1e0814f5",
      "durability":"Ephemeral"
     },
     "type":"Full",
     "names":[
      {
       "salutation":null,
       "first_name":"Bob",
       "middle_name":"S",
       "last_name":"Bobson",
       "suffix":null,
       "valid_for":null
      }
     ],
     "age_range":null,
     "gender":null,
     "locations":[],
     "phones":[
      {
       "id":{
        "key":"Phone.ec7f6fef-a2e2-4b08-cfe3-bc7128b46deb.Durable",
        "url":"https://proapi.whitepages.com/2.1/entity/Phone.ec7f6fef-a2e2-4b08-cfe3-bc7128b46deb.Durable.json?api_key=fa4bbd5febebc9849fe32bc80c6ee892",
        "type":"Phone",
        "uuid":"ec7f6fef-a2e2-4b08-cfe3-bc7128b46deb",
        "durability":"Durable"
       },
       "line_type":"Mobile",
       "belongs_to":null,
       "associated_locations":null,
       "is_valid":true,
       "country_calling_code":"1",
       "extension":null,
       "carrier":"Verizon Wireless",
       "do_not_call":true,
       "reputation":{
        "spam_score":2,
        "spam_index":1,
        "level":1,
        "details":[
         {
          "score":2,
          "type":"Uncertain",
          "category":"Unknown"
         }
        ]
       },
       "is_prepaid":null,
       "is_connected":true,
       "best_location":null,
       "valid_for":null,
       "contact_type":null,
       "contact_creation_date":null
      }
     ],
     "best_name":"Bob S Bobson",
     "best_location":null,
     "valid_for":null,
     "is_historical":false
    }
   ],
   "associated_locations":[
    {
     "id":{
      "key":"Location.8e278077-301f-487f-8a26-aa18d27ca43e.Durable",
      "url":"https://proapi.whitepages.com/2.1/entity/Location.8e278077-301f-487f-8a26-aa18d27ca43e.Durable.json?api_key=fa4bbd5febebc9849fe32bc80c6ee892",
      "type":"Location",
      "uuid":"8e278077-301f-487f-8a26-aa18d27ca43e",
      "durability":"Durable"
     },
     "type":"Address",
     "valid_for":null,
     "legal_entities_at":null,
     "city":"Anytown",
     "postal_code":"01234",
     "zip4":"4444",
     "state_code":"CA",
     "country_code":"US",
     "address":"3434 Bubble Ct, Anytown CA 01234-4444",
     "house":"3434",
     "street_name":"Bubble",
     "street_type":"Ct",
     "pre_dir":null,
     "post_dir":null,
     "apt_number":null,
     "apt_type":null,
     "box_number":null,
     "is_receiving_mail":true,
     "not_receiving_mail_reason":null,
     "usage":"Residential",
     "delivery_point":"SingleUnit",
     "box_type":null,
     "address_type":"Street",
     "lat_long":{
      "latitude":24.688217,
      "longitude":-106.167145,
      "accuracy":"RoofTop"
     },
     "is_deliverable":true,
     "standard_address_line1":"3434 Bubble Ct",
     "standard_address_line2":"",
     "standard_address_location":"Anytown CA 01234-4444",
     "is_historical":false,
     "contact_type":null,
     "contact_creation_date":null
    }
   ],
   "is_valid":true,
   "country_calling_code":"1",
   "extension":null,
   "carrier":"Verizon Wireless",
   "do_not_call":true,
   "reputation":{
    "spam_score":2,
    "spam_index":1,
    "level":1,
    "details":[
     {
      "score":2,
      "type":"Uncertain",
      "category":"Unknown"
     }
    ]
   },
   "is_prepaid":null,
   "is_connected":true,
   "best_location":{
    "id":{
     "key":"Location.8e278077-301f-487f-8a26-aa18d27ca43e.Durable",
     "url":"https://proapi.whitepages.com/2.1/entity/Location.8e278077-301f-487f-8a26-aa18d27ca43e.Durable.json?api_key=fa4bbd5febebc9849fe32bc80c6ee892",
     "type":"Location",
     "uuid":"8e278077-301f-487f-8a26-aa18d27ca43e",
     "durability":"Durable"
    },
    "type":"Address",
    "valid_for":null,
    "legal_entities_at":null,
    "city":"Anytown",
    "postal_code":"01234",
    "zip4":"4444",
    "state_code":"CA",
    "country_code":"US",
    "address":"3434 Bubble Ct, Anytown CA 01234-4444",
    "house":"3434",
    "street_name":"Bubble",
    "street_type":"Ct",
    "pre_dir":null,
    "post_dir":null,
    "apt_number":null,
    "apt_type":null,
    "box_number":null,
    "is_receiving_mail":true,
    "not_receiving_mail_reason":null,
    "usage":"Residential",
    "delivery_point":"SingleUnit",
    "box_type":null,
    "address_type":"Street",
    "lat_long":{
     "latitude":24.688217,
     "longitude":-106.167145,
     "accuracy":"RoofTop"
    },
    "is_deliverable":true,
    "standard_address_line1":"3434 Bubble Ct",
    "standard_address_line2":"",
    "standard_address_location":"Anytown CA 01234-4444"
   }
  }
 ],
 "messages":[]
}
"""


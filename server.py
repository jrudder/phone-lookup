"""
Simple Server for FPA

Sample EveryoneAPI Output
=========================
{
    "data": {
      "address": "15 Robin Hood Lane",
      "carrier": {
      "id": "214",
      "name": "Growing Wireless Inc."
    },
    "carrier_o": {
      "id": "213",
      "name": "Paine Mobile Inc."
    },
    "cnam": "MICHAEL SEAVER",
    "expanded_name": {
      "first": "Michael",
      "last": "Seaver"
    },
    "gender": "M",
    "image": {
      "cover": "//teloimg-pub.com.s3.amazonaws.com/cover.jpg",
      "large": "//teloimg-pub.com.s3.amazonaws.com/large.jpg",
      "med": "//teloimg-pub.com.s3.amazonaws.com/med.jpg",
      "small": "//teloimg-pub.com.s3.amazonaws.com/small.jpg"
    },
    "line_provider": {
      "name": "MysticVoice",
      "ocn": "215"
    },
    "linetype": "mobile",
    "location": {
      "city": "Long Island",
      "geo": {
        "latitude": "40.799787",
        "longitude": "-73.971421"
      },
      "state": "NY",
      "zip": "10003"
    },
    "name": "Michael Seaver",
    "profile": {
      "edu": "Thomas Dewey High School",
      "job": "Custodian",
      "relationship": "April Lerman"
    }
    },
    "note": "THIS IS A SAMPLE, YOU WILL NOT BE CHARGED",
    "pricing": {
      "breakdown": {
        "address": -0.08,
        "carrier": -0.002,
        "carrier_0": 0,
        "cnam": -0.005,
        "gender": -0.001,
        "image": -0.02,
        "line_provider": -0.005,
        "linetype": -0.001,
        "location": 0,
        "name": -0.01,
        "profile": -0.005
      },
      "total": -0.12900000000000003
    },
    "status": true,
    "type": "person"
  }
"""

# Python
import functools
import logging
from wsgiref.simple_server import make_server
# Pyramid
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.httpexceptions import HTTPException, HTTPUnauthorized, HTTPBadRequest
# 3rd Party
import simplejson as json
# * * *
from vendor import Vendor
from vendor_mock import MockVendor

log = logging.getLogger(__name__)

VENDORS = []
SID = "123"
TOKEN = "456"

def api(request):
  try:
    # Parse the request
    params = _parse_request(request)

    # Remove auth stuff
    del params["sid"]
    del params["token"]

    # Perform the lookup
    lookdown_result = _lookdown(VENDORS, **params)
    if lookdown_result is None:
      response = "[]"
    else:
      response = {
        "data": lookdown_result
      }

    result = Response(json.dumps(response))

  except HTTPException as exc:
    result = exc
    result.text = exc.detail
    
  except:
    log.error("Server Error", exc_info=True)
    result = Response("Server error", status=500)

  result.content_type = "application/json"
  return result

def _parse_request(request):
  """
  Parse the request
  """

  global SID
  global TOKEN
  
  try:
    sid        = request.params["sid"]
    token      = request.params["token"]
    address    = request.params["address"]
    city       = request.params["city"]
    state      = request.params["state"]
    postalCode = request.params["postalCode"]
    country    = request.params["country"]

    result = {
      "sid": sid,
      "token": token,
      "address": address,
      "city": city,
      "state": state,
      "postalCode": postalCode,
      "country": country,
    }

    if not (sid==SID and token==TOKEN):
      raise HTTPUnauthorized('{"status":"unauthorized"}')

  except KeyError as exc:
    raise HTTPBadRequest('{{"missing":"{}"}}'.format(exc.args[0]))

  return result

def _lookdown(vendors, address, city, state, postalCode, country):
  """
  Perform the forward phone append
  """

  result = None
  for v in vendors:
    lookdown_result = v.lookdown(address, city, state, postalCode, country)
    if lookdown_result.success:
      result = lookdown_result.contacts
      break

  return result

def serve(vendors, sid=None, token=None):
  global VENDORS
  global SID
  global TOKEN
  VENDORS = vendors

  if sid is None: sid = "1234"
  if token is None: token = "5678"
  SID = sid
  TOKEN = token
  
  # Configure and run the Pyramid app
  config = Configurator()
  config.add_route("api", "/api")
  config.add_view(api, route_name="api")
  app = config.make_wsgi_app()
  server = make_server("0.0.0.0", 8080, app)
  server.serve_forever()

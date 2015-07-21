"""
Test the Server
"""

# Python
from unittest.mock import patch
# Pyramid
from pyramid.testing import DummyRequest
# * * *
import server

def test_parser():
  """ Ensure that the request parser works """

  request = DummyRequest()
  request.params = {
    "sid": "123",
    "token": "456",
    "address": "123 Main St",
    "city": "Anytown",
    "state": "NY",
    "country": "US",
    "postalCode": "12345"}

  req = server._parse_request(request)
  assert req["sid"] == "123"
  assert req["token"] == "456"
  assert req["address"] == "123 Main St"

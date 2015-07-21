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
  request.params = {"token": "123", "name": "bob smith", "addr": "123 Main St"}

  auth, name, addr = server._parse_request(request)
  assert auth == "123"
  assert name == "bob smith"
  assert addr == "123 Main St"

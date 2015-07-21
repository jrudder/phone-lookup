"""
Mock Vendor
"""
# Python
import logging
# * * *
from vendor import Vendor

log = logging.getLogger(__name__)

@Vendor.register(name="mock")
class MockVendor(Vendor):
  
  def __init__(self, config):
    if "name" in config:
      self.name = config["name"]
    else:
      self.name = "mock"

  def lookup(self, number):
    """
    Perform a lookup of a number

    Args:
      number (str): phone number to lookup

    Returns:
      LookupResult
    """

    return Vendor.LookupResult(
      success=True,
      contacts=[{
        "firstname": "Sally", "lastname": "Smith",
        "address": "123 Main St", "city": "Anytown", "state": "CA", "country": "USA", "zip": "01234"
      }
    ])

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

    return Vendor.LookdownResult(
      success=True,
      contacts=[{
        "firstname": "Sally", "lastname": "Smith",
        "address": "123 Main St", "city": "Anytown", "state": "CA", "country": "USA", "zip": "01234",
        "number": "3105551234"
      }
    ])

  def name(self):
    """
    Return a unique representation for the vendor
    """
    return self.name

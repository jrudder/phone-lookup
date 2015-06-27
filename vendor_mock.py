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
    Perform a lookup

    Args:
      number (str): phone number to lookup

    Returns:
      LookupResult
    """

    return Vendor.LookupResult(
      success=True,
      contacts=[
        {"firstname": "Sally", "lastname": "Smith", "address": "123 Main St", "city": "Anytown", "zip": "01234"}
      ])

  def name(self):
    """
    Return a unique representation for the vendor
    """
    return self.name

  def self_test(self):
    """ Nothing to test """
    pass
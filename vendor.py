"""
Vendor

This is the plugin handler for reverse- and forward- phone append vendors.

To add a new vendor, simply:

1. create a new class and register it (see vendor_mock.py for a simple example
2. add an instance of the class to the output of get_waterfall in main.py
3. add any required command line arguments (e.g. for API keys)
4. Enjoy!
"""
# Python
from abc import ABCMeta
from abc import abstractmethod
from collections import namedtuple
import logging
# * * *
from provider_base import ProviderBase

log = logging.getLogger(__name__)

class Vendor(ProviderBase, metaclass=ABCMeta):
  # Registered providers get added to this dict
  providers = {}

  LookupResult  = namedtuple("LookupResult", [
    "success",          # bool: True if the lookup was successful
    "contacts",         # array of contacts with name and address
  ])
  LOOKUP_FAILED = LookupResult(success=False, contacts=None)

  LookdownResult  = namedtuple("LookdownResult", [
    "success",          # bool: True if the lookup was successful
    "contacts",         # array of contacts with name and address
  ])
  LOOKDOWN_FAILED = LookdownResult(success=False, contacts=None)

  @abstractmethod
  def lookup(self, number):
    """
    Perform a lookup

    Args:
      number (str): phone number to lookup

    Returns:
      LookupResult
    """
    raise NotImplementedError("Implement this method in the child class")

  @abstractmethod
  def lookdown(self, address, city, state, postalCode, country):
    """
    Perform a lookup of name and address to phone

    Args:
      address (str): line1 and line2 of the address to lookup
      city (str): city of the address to lookup
      state (str): state of the address to lookup
      postalCode (str): five- or nine-digit postal code of the address to lookup
      country (str): two-character ISO country code

    Returns:
      LookdownResult
    """
    raise NotImplementedError("Implement this method in the child class")

  @abstractmethod
  def name(self):
    """
    Return a unique representation for the vendor
    """
    raise NotImplementedError("Implement this method in the child class")

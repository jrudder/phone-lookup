"""
Vendor
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
  def name(self):
    """
    Return a unique representation for the vendor
    """
    raise NotImplementedError("Implement this method in the child class")

  @abstractmethod
  def self_test(self):
    """
    Test yourself
    """
    raise NotImplementedError("Implement this method in the child class")
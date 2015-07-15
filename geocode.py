"""
Geocode

This is the plugin manager for address geocoding.
"""
# Python
from abc import ABCMeta
from abc import abstractmethod
from collections import namedtuple
import logging
# * * *
from provider_base import ProviderBase

log = logging.getLogger(__name__)

class Geocoder(ProviderBase, metaclass=ABCMeta):
  # Registered providers get added to this dict
  providers = {}

  GeocodeResult  = namedtuple("GeocodeResult", [
    "success",          # bool: True if the geocoding was successful
    "formatted",        # str: formatted address
    "accuracy_str",     # str: plugin-specific level of geocoding accuracy
    "latitude",         # float: latitude of the geocoded point
    "longitude",        # float: longitude of the geocoding point
  ])
  GEOCODE_FAILED = GeocodeResult(success=False, formatted=None, accuracy_str=None, latitude=None, longitude=None)

  @abstractmethod
  def geocode(self, *, line1, line2=None, city, region, country, postalCode):
    """
    Geocode the address

    Args:
      line1 (str): primary address line (e.g. "123 Main St")
      line2 (str): optional second address line (e.g. "Apt #13")
      city (str): city (e.g. "Beverly Hills")
      region (str): region or US state (e.g. "California")
      country (str): ISO-3 country code (e.g. "USA")
      postalCode (str): five- or nine-digit postal code (e.g. "90210")

    Returns:
      GeocodeResult
    """
    raise NotImplementedError("Implement this method in the child class")

  @property
  def name(self):
    """ Return the geocoder's registered name """
    # Return the _name property added by ProviderBase upon registration
    return self._name

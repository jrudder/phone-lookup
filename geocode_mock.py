"""
Mock Geocoder
"""
# Python
import logging
# * * *
from geocode import Geocoder

log = logging.getLogger(__name__)

@Geocoder.register(name="mock")
class MockGeocoder(Geocoder):
  
  def __init__(self, config):
    pass
  
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
    formatted = "{address} {city} {region} {country} {postalCode}".format(
        address = line1 if line2 is None else "{} {}".format(line1, line2),
        city       = city,
        region     = region,
        country    = country,
        postalCode = postalCode)

    result = Geocoder.GeocodeResult(
      success=True,
      formatted=formatted,
      accuracy_str="mock_POINT",
      latitude=33.8120918,
      longitude=-117.9189742)

    #except:
    #  result = Geocoder.GEOCODE_FAILED
   
    return result
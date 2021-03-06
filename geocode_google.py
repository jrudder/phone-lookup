"""
Google Geocoder
"""
# Python
import logging
# 3rd Party
from pygeocoder import Geocoder as PyGeocoder
from pygeocoder import GeocoderError
# * * *
from geocode import Geocoder

log = logging.getLogger(__name__)

@Geocoder.register(name="google")
class GoogleGeocoder(Geocoder):
  
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

    try:
      if line1 is None:
        address = ""
      elif line2 is None:
        address = line1
      else:
        address = "{} {}".format(line1, line2)
      
      g = PyGeocoder.geocode("{address} {city} {region} {country} {postalCode}".format(
        address    = address,
        city       = city,
        region     = region,
        country    = country,
        postalCode = postalCode,
      ))

      log.info(g.data)

      result = Geocoder.GeocodeResult(
        success=True,
        formatted=g.formatted_address,
        accuracy_str=g.location_type,
        latitude=g.latitude,
        longitude=g.longitude)

    except GeocoderError:
      log.error("Failed to geocode", exc_info=True)
      result = Geocoder.GEOCODE_FAILED
   
    return result

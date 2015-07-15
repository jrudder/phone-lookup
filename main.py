#!/usr/bin/env python3
"""
Run some phone numbers through some APIs, storing the results in a JSON file.

Usage:
python main.py --pceid <ACCESS ID>

JSON format:
[
  {
    "number": "3105550123",
    "vendor": "VendorName",
    "contacts": [
      {
        "name": "Sally Smith",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "JR",
        "zip": 12345
      }
      ...
    ]
    "vendors_checked": [
      "Vendor A",
      "Vendor B",
      "Vendor C"
    ]
  },
  ...
]
"""

# Python
import argparse
import json
import logging
import signal
# * * *
from vendor import Vendor
from vendor_mock import MockVendor
from vendor_pacificeast import PacificEast
from geocode import Geocoder
from geocode_mock import MockGeocoder
from geocode_google import GoogleGeocoder

log = logging.getLogger(__name__)

SIGINT_caught = False

def main():
  """
  Do it
  """

  # Parse the command line args
  parser = argparse.ArgumentParser(description="Phone Lookup")
  # What to do
  parser.add_argument("--lookup",   action="store_true", help="Perform phone lookup?")
  parser.add_argument("--geocode",  action="store_true", help="Perform geocoding?")

  # Which geocoder to use
  parser.add_argument("--geocoder", type=str, default="mock", help="Which geocoder ('mock' or 'google')")

  parser.add_argument("--pceid",    type=str,            help="PacificEast Account ID/Key")
  parser.add_argument("--runall",   action="store_true", help="Run all numbers without prompting")
  args = parser.parse_args()

  # Get the waterfall
  waterfall = get_waterfall(pce_id=args.pceid)

  # Perform lookups
  if not (args.lookup or args.geocode):
    log.warn("No actions specified. Use '--lookup' and/or '--geocode' to do something.")
  else:
    # Load the number data and perform the lookups
    log.debug("Loading numbers.json")
    numbers = load_numbers("numbers.json")

    if args.lookup:
      log.info("Performing lookups")
      do_lookups(numbers, waterfall, "numbers.json", runall=args.runall)

    if args.geocode:
      log.info("Performing geocoding")
      geocoder = Geocoder.get(args.geocoder, config={})
      do_geocoding(numbers, geocoder, "numbers.json", runall=args.runall)

def get_waterfall(pce_id):
  """
  Create the lookup waterfall

  Args:
    None

  Returns:
    [{}]: list of dicts with keys name (str), config (dict) where
          name is the name of a Vendor provider and config is the associated configuration
  """
  waterfall = [
    Vendor.get("mock", config={}),
    #Vendor.get("PacificEast", config={"public": False, "account_id": pce_id}),
    #Vendor.get("PacificEast", config={"public": True,  "account_id": pce_id}),
  ]

  return waterfall

def load_numbers(path):
  """
  Load the phone numbers from the file

  Args:
    path (str): path of the JSON file to read and parse

  Returns:
    [str]: list of strings of phone numbers
  """

  # Load the data
  with open(path) as f:
    result = json.load(f)

  return result

def do_lookups(numbers, waterfall, save_file, runall=False):
  """
  Perform lookups on those numbers that have no lookup data

  NOTE: numbers is modified in-place!

  Args:
    numbers (dict): numbers to check
    waterfall (list of Vendors): vendors to use for lookups
    save_file (str): path to the file to be used for storing intermediate results
    runall (bool): run without prompting (default is to prompt for each number)

  Returns:
    None
  """

  for number in numbers:
    # Only lookup numbers that don't have data
    if number.get("vendor", None) is None:
      for vendor in waterfall:
        if vendor.name not in number.setdefault("vendors_checked", []):
          if not runall:
            check_keep_going("Lookup", number["number"], vendor.name)
          else:
            log.debug("Lookup of {} at {}".format(number["number"], vendor.name))

          # Perform the lookup
          number.get("vendors_checked", []).append(vendor.name)
          lookup = vendor.lookup(number["number"])

          # Store the results on the number
          if lookup.success:
            # Success
            number["vendor"]   = vendor.name
            number["contacts"] = lookup.contacts

          # Save the numbers
          write_results(numbers, save_file)

          # Stop searching for this number if we got a result
          if lookup.success: break

def do_geocoding(numbers, geocoder, save_file, runall=False):
  """
  Perform geocoding on those numbers that have an address but no lat/lng

  NOTE: numbers is modified in-place!

  Args:
    numbers (dict): numbers to check
    geocoder (Geocoder): geocoder to be used for lookups
    save_file (str): path to the file to be used for storing intermediate results
    runall (bool): run without prompting (default is to prompt for each number)

  Returns:
    None
  """

  for number in numbers:
    # Only geocode numbers with an address that has not been geocoded
    for contact in number.get("contacts", []):
      if contact.get("address", None) is not None and contact.get("geocoded", False) is False:
        if not runall:
          check_keep_going("Geocode", number["number"], geocoder.name)
        else:
          log.debug("Geocoding {} with {}".format(number["number"], geocoder.name))

        # Perform the lookup
        contact["geocoded"] = True
        lookup = geocoder.geocode(
          line1 = contact["address"],
          city = contact["city"],
          region = contact["state"],
          country = contact["country"],
          postalCode = contact["zip"])

        # Store the results on the contact
        if lookup.success:
          # Success
          contact["formatted_addr"] = lookup.formatted
          contact["geo_accuracy"] = lookup.accuracy_str
          contact["latitude"]  = lookup.latitude
          contact["longitude"] = lookup.longitude

        # Save the numbers
        write_results(numbers, save_file)

def write_results(numbers, filepath):
  """
  Write the numbers result to the file

  Args:
    numbers (dict): dict of phone (str), vendor (str), restricted (bool), name (str), address (str)
    file (File object): if None use sys.stdout

  Returns:
    None
  """

  log.debug("Saving numbers.json")

  # Update the file
  with open("numbers.json", "w") as f:
    json.dump(numbers, f, indent=2)

  # Check for SIGINT
  if SIGINT_caught:
    print("SIGINT caught")
    exit(1)

def check_keep_going(operation, number, vendor):
  """
  Prompt to continue or stop
  """
  while True:
    c = input("{} {} with {}? ".format(operation, number, vendor))
    if c == "y":
      return None
    elif c == "n":
      exit(1)

def log_to_stdout():
  """ Enable logging to stdout """
  import sys

  root = logging.getLogger()
  root.setLevel(logging.DEBUG)

  ch = logging.StreamHandler(sys.stdout)
  ch.setLevel(logging.DEBUG)
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
  ch.setFormatter(formatter)
  root.addHandler(ch)

if __name__ == "__main__":
  # Handle SIGINT gracefully
  def signal_handler(signal, frame):
    global SIGINT_caught
    SIGINT_caught = True
  signal.signal(signal.SIGINT, signal_handler)

  # Enable logging to stdout
  log_to_stdout()

  # Do it.
  main()

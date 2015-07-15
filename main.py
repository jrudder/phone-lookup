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

log = logging.getLogger(__name__)

SIGINT_caught = False

def main():
  """
  Do it
  """

  # Parse the command line args
  parser = argparse.ArgumentParser(description="Phone Lookup")
  parser.add_argument("--pceid",    type=str,            help="PacificEast Account ID/Key")
  parser.add_argument("--runall",   action="store_true", help="Run all numbers without prompting")
  args = parser.parse_args()

  # Get the waterfall
  waterfall = get_waterfall(pce_id=args.pceid)

  # Load the number data and perform the lookups
  numbers = load_numbers("numbers.json")
  do_lookups(numbers, waterfall, "numbers.json", runall=args.runall)

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
    #Vendor.get("mock", config={}),
    Vendor.get("PacificEast", config={"public": False, "account_id": pce_id}),
    Vendor.get("PacificEast", config={"public": True,  "account_id": pce_id}),
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

def do_lookups(numbers, waterfall, tmp_file, runall=False):
  """
  Perform lookups on those numbers that have no lookup data

  NOTE: numbers is modified in-place!

  Args:
    numbers: 
  """

  for number in numbers:
    # Only lookup numbers that don't have data
    if number.get("vendor", None) is None:
      for vendor in waterfall:
        if vendor.name not in number.setdefault("vendors_checked", []):
          if not runall:
            check_keep_going(number["number"], vendor.name)
          else:
            print("Lookup of {} at {}".format(number["number"], vendor.name))

          # Perform the lookup
          number.get("vendors_checked", []).append(vendor.name)
          lookup = vendor.lookup(number["number"])

          # Store the results on the number
          if lookup.success:
            # Success
            number["vendor"]   = vendor.name
            number["contacts"] = lookup.contacts

          # Save the numbers
          write_results(numbers, tmp_file)

          # Stop searching for this number if we got a result
          if lookup.success: break

def write_results(numbers, filepath):
  """
  Write the numbers result to the file

  Args:
    numbers (dict): dict of phone (str), vendor (str), restricted (bool), name (str), address (str)
    file (File object): if None use sys.stdout

  Returns:
    None
  """

  # Update the file
  with open("numbers.json", "w") as f:
    json.dump(numbers, f, indent=2)

  # Check for SIGINT
  if SIGINT_caught:
    print("SIGINT caught")
    exit(1)

def check_keep_going(number, vendor):
  """
  Prompt to continue or stop
  """
  while True:
    c = input("Lookup {} with {}? ".format(number, vendor))
    if c == "y":
      return None
    elif c == "n":
      exit(1)

if __name__ == "__main__":
  # Handle SIGINT gracefully
  def signal_handler(signal, frame):
    global SIGINT_caught
    SIGINT_caught = True

  signal.signal(signal.SIGINT, signal_handler)

  # Do it.
  main()

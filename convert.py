#!/usr/bin/env python3
"""
Convert the JSON to CSV
"""

# Python
import csv
import json

FILENAME = "numbers5"

def main():
  """
  Do it
  """

  numbers = load_json("{}.json".format(FILENAME))
  write_csv("{}.csv".format(FILENAME), numbers)

def load_json(path):
  """
  Load the numbers JSON from path
  """
  with open("{}.json".format(FILENAME)) as f:
    numbers = json.load(f)

  return numbers

def write_csv(path, numbers):
  """
  Write the numbers data as CSV to path
  """
  with open(path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["number", "firstname", "lastname", "address", "city", "state", "zip", "latitude", "longitude", "vendor", "restricted"])
    for n in numbers:
      if len(n.get("contacts", [])) == 0:
        writer.writerow([n["number"]])
      else:
        for c in n["contacts"]:
          writer.writerow([
              n["number"],
              c.get("firstname", ""),
              c.get("lastname", ""),
              c.get("address", ""),
              c.get("city", ""),
              c.get("state", ""),
              c.get("zip", ""),
              c.get("latitude", ""),
              c.get("longitude", ""),
              n.get("vendor", "-").split("-")[0],
              "Y" if "restricted" in n.get("vendor", "") else "N"])

if __name__ == "__main__":
  # Do it.
  main()

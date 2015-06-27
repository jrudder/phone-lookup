#!/usr/bin/env python3
"""
Convert the JSON to CSV
"""

# Python
import csv
import json

def main():
  """
  Do it
  """

  numbers = load_json("numbers.json")
  write_csv("numbers.csv", numbers)

def load_json(path):
  """
  Load the numbers JSON from path
  """
  with open("numbers.json") as f:
    numbers = json.load(f)

  return numbers

def write_csv(path, numbers):
  """
  Write the numbers data as CSV to path
  """
  with open(path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["number", "name", "address", "city", "state", "zip"])
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
              c.get("zip", "")])

if __name__ == "__main__":
  # Do it.
  main()

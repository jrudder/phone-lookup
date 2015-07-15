# Phone Lookup

Quickstart
==========
This has been tested on Python 3.4.2. This should get you going:

```
virtualenv -p `which python3` .env
source .env/bin/activate
pip install -r requirements.txt
python main.py -h
```

If all is well, you'll see something like this:
```
usage: main.py [-h] [--pceid PCEID] [--runall]

Phone Lookup

optional arguments:
  -h, --help     show this help message and exit
  --pceid PCEID  PacificEast Account ID/Key
  --runall       Run all numbers without prompting
```

To run, simply pass the ```--pceid``` flag with the PacificEast access id. You'll be prompted before each lookup.
Type ```y``` and press ```ENTER``` to perform the lookup or ```n```` to quit. Before anything will work, you'll need
a working input file. See below.

numbers.json
============
The program expects to find ```numbers.json``` in the same directory. It should look like this:

```
[
  {"number": "2135550123"},
  {"number": "2125554567"},
  ...
]
```

After being run, it will look more like this:

```
[
  {
    "number": "3105550123",             # number queried
    "vendor": "VendorName",             # vendor that hit
    "contacts": [                       # details of each hit
      {
        "name": "Sally Smith",
        "address": "123 Main St",
        "city": "Anytown",
        "state": "JR",
        "zip": 12345
      }
      ...
    ]
    "vendors_checked": [                # list of vendors already queried
      "Vendor A",
      "Vendor B",
      "Vendor C"
    ]
  },
  ...
]
```

CSV
===
To convert ```numbers.json``` to ```numbers.csv```, just run ```./convert.py```

New Vendors
===========
To add a new vendor, simply:

1. create a new class and register it (see ```vendor_mock.py``` for a simple example
2. add an instance of the class to the output of ```get_waterfall``` in ```main.py```
3. add any required command line arguments (e.g. for API keys)
4. Enjoy!
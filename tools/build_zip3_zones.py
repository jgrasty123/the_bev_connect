#!/usr/bin/env python3
"""
Build assets/data/zip3-zones-930.json from the UPS zone chart for origin 930.

The UPS zone chart is the authoritative ZIP3 -> zone source for our Ventura
origin. Do NOT hand-build this file from state guesses.

How to get the source file
--------------------------
Download either of these in a browser (UPS blocks automated fetches):

  https://www.ups.com/media/us/currentrates/zone-txt/930.txt

  ...or use the UPS Zone Chart tool and export the CSV for origin 930:
  https://www.ups.com/us/en/support/shipping-support/shipping-costs-rates/zone-chart.page

Save it as tools/ups-zone-930.txt (or .csv) and run:

    python3 tools/build_zip3_zones.py tools/ups-zone-930.txt

Input format
------------
UPS ships a comma-delimited table whose first column is a destination ZIP3
(or a hyphenated ZIP3 range) and whose remaining columns are zones per
service. Ground is the first zone column. Example rows:

    Dest. ZIP,Ground,3 Day Select,2nd Day Air,...
    004-005,8,308,208,...
    010-041,8,308,208,...
    900,2,302,202,...

Ranges are expanded to one entry per ZIP3. Rows whose Ground column is "-"
(no Ground service) are skipped and reported, so they surface as
"request a quote" rather than silently defaulting to a zone.
"""

import csv
import json
import os
import re
import sys

OUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "data", "zip3-zones-930.json",
)

# Zones we can actually price against weship-ground-rates-2025.json
VALID_ZONES = {2, 3, 4, 5, 6, 7, 8, 44, 45, 46}

ZIP3_ROW = re.compile(r"^\s*(\d{3})(?:\s*-\s*(\d{3}))?\s*$")


def parse(path):
    zones = {}
    skipped = []
    unexpected = []

    with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row or len(row) < 2:
                continue

            m = ZIP3_ROW.match(row[0].strip().strip('"'))
            if not m:
                continue  # header / preamble line

            raw = row[1].strip().strip('"')
            if raw in ("-", "", "[1]"):
                skipped.append(row[0].strip())
                continue

            try:
                zone = int(raw)
            except ValueError:
                unexpected.append((row[0].strip(), raw))
                continue

            if zone not in VALID_ZONES:
                unexpected.append((row[0].strip(), raw))
                continue

            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else start
            for n in range(start, end + 1):
                zones["%03d" % n] = zone

    return zones, skipped, unexpected


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    src = sys.argv[1]
    if not os.path.exists(src):
        sys.exit("Source file not found: %s" % src)

    zones, skipped, unexpected = parse(src)

    if not zones:
        sys.exit(
            "No ZIP3 rows parsed. Check that %s is the UPS zone chart for "
            "origin 930 and not an HTML error page." % src
        )

    payload = {
        "_meta": {
            "origin_zip3": "930",
            "origin": "Ventura, CA 93003",
            "service": "UPS Ground",
            "source_file": os.path.basename(src),
            "zip3_count": len(zones),
        },
        "zones": zones,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")

    print("Wrote %s" % OUT_PATH)
    print("  ZIP3 prefixes mapped : %d" % len(zones))
    print("  distinct zones       : %s" % sorted(set(zones.values())))
    if skipped:
        print("  no Ground service    : %d rows (%s...)"
              % (len(skipped), ", ".join(skipped[:6])))
    if unexpected:
        print("  UNEXPECTED zone values (review these):")
        for z3, val in unexpected[:20]:
            print("    %s -> %r" % (z3, val))

    # Sanity: our own back yard should be a low zone.
    local = zones.get("930")
    if local is not None and local > 3:
        print("  WARNING: ZIP3 930 resolved to zone %d — expected 2. "
              "Wrong origin chart?" % local)


if __name__ == "__main__":
    main()

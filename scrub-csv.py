"""
.csv Column Scrubbing

PURPOSE
---
Replaces values in specified columns of a headerless CSV dump (exported via pg_dump) with the string "REDACTED". Empty fields are left untouched.
The output file is written alongside the input file with "_PII_SCRUBBED" appended to the filename.

USAGE
---
    python scrub_pii.py <input.csv> <col1,col2,...>

ARGUMENTS
---
    input.csv       : Path to the raw pg_dump CSV file (no header).
    col1,col2,...   : Comma-separated list of column positions to scrub.

NOTES
-----
    - Column positions are 1-based (first column = 1).
    - Rows with fewer columns than the highest specified index are written as-is with a WARNING.
    - This script is safe to re-run; each run overwrites the previous output.

WORKFLOW
--------
    1. Identify which column positions contain PII 
    2. Run this script against the pg_dump CSV.
        EXAMPLE - python scrub_pii.py file_name.csv 4,6,7,10,11,12,30
    3. Verify the output looks correct (spot-check a few rows).
    4. Use the _PII_SCRUBBED.csv as the source for pg_restore.
"""

import csv
import sys
from pathlib import Path

REDACTED = "REDACTED"


def parse_columns(raw: str) -> set[int]:
    indices = set()
    invalid = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit() and int(part) >= 1:
            indices.add(int(part) - 1)  # convert to 0-based
        else:
            invalid.append(part)
    if invalid:
        print(f"ERROR: Invalid column position(s): {', '.join(invalid)}")
        print("Column positions must be integers >= 1.")
        sys.exit(1)
    return indices


def scrub(input_path: str, columns_to_scrub: set[int]):
    input_file = Path(input_path)

    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    output_file = input_file.parent / f"PII_SCRUBBED_{input_file.name}"
    max_col_index = max(columns_to_scrub)

    rows_processed = 0
    rows_scrubbed = 0

    with open(input_file, newline="", encoding="utf-8") as infile, \
        open(output_file, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            if len(row) <= max_col_index:
                print(f"WARNING: Row {rows_processed + 1} has only {len(row)} columns "
                    f"(expected at least {max_col_index + 1}), writing as-is")
                writer.writerow(row)
                rows_processed += 1
                continue

            had_pii = False
            scrubbed_row = []

            for i, value in enumerate(row):
                if i in columns_to_scrub and value.strip():
                    scrubbed_row.append(REDACTED)
                    had_pii = True
                else:
                    scrubbed_row.append(value)

            writer.writerow(scrubbed_row)
            rows_processed += 1
            if had_pii:
                rows_scrubbed += 1

    print(f"Done. {rows_processed} rows processed, {rows_scrubbed} rows had PII scrubbed.")
    print(f"Output written to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scrub_pii.py <input.csv> <col1,col2,...>")
        print("Example: python scrub_pii.py registered_owner.csv 4,6,7,10,11,12,30")
        sys.exit(1)

    scrub(sys.argv[1], parse_columns(sys.argv[2]))

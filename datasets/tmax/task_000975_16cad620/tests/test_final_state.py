# test_final_state.py

import os
import re
import csv
import glob
import pytest

def get_expected_translations():
    """
    Reads all .jsonl files in /home/user/locales/ and computes the expected
    valid translations based on the rules.
    """
    jsonl_files = glob.glob("/home/user/locales/*.jsonl")
    valid_records = []

    line_pattern = re.compile(r'\{\s*"msgid"\s*:\s*"([^"]+)"\s*,\s*"msgstr"\s*:\s*"([^"]+)"\s*\}')

    for file_path in jsonl_files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = line_pattern.search(line)
                if not match:
                    continue
                msgid, msgstr = match.groups()

                # Validation: check all \u occurrences
                # Find all indices of '\u'
                is_valid = True
                idx = 0
                while True:
                    idx = msgstr.find('\\u', idx)
                    if idx == -1:
                        break
                    # Check if the next 4 characters are hex digits
                    hex_part = msgstr[idx+2:idx+6]
                    if len(hex_part) != 4 or not all(c in '0123456789abcdefABCDEF' for c in hex_part):
                        is_valid = False
                        break
                    idx += 2 # move past the '\u'

                if is_valid:
                    valid_records.append((msgid, msgstr))

    return valid_records

def test_files_exist():
    """Verify that the required source, executable, and script files exist."""
    assert os.path.exists("/home/user/loc_parser.c"), "C source file /home/user/loc_parser.c is missing."
    assert os.path.exists("/home/user/loc_parser"), "Compiled executable /home/user/loc_parser is missing."
    assert os.access("/home/user/loc_parser", os.X_OK), "/home/user/loc_parser is not executable."
    assert os.path.exists("/home/user/process_locales.sh"), "Shell script /home/user/process_locales.sh is missing."
    assert os.access("/home/user/process_locales.sh", os.X_OK), "/home/user/process_locales.sh is not executable."

def test_output_csv_exists():
    """Verify that the output CSV file was created."""
    assert os.path.exists("/home/user/valid_translations.csv"), "Output file /home/user/valid_translations.csv is missing."

def test_output_csv_content():
    """Verify the header and the data lines of the output CSV."""
    csv_path = "/home/user/valid_translations.csv"
    assert os.path.exists(csv_path), "Cannot check content, CSV missing."

    with open(csv_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, "CSV file is empty."
    assert lines[0] == "msgid,msgstr", f"Incorrect header in CSV. Expected 'msgid,msgstr', got '{lines[0]}'."

    expected_records = get_expected_translations()
    expected_lines = set(f"{msgid},{msgstr}" for msgid, msgstr in expected_records)

    actual_lines = set(lines[1:])

    missing = expected_lines - actual_lines
    extra = actual_lines - expected_lines

    assert not missing, f"Missing expected valid translations in CSV: {missing}"
    assert not extra, f"Found extra (possibly invalid) translations in CSV: {extra}"
    assert len(lines) - 1 == len(expected_records), f"Expected exactly {len(expected_records)} data lines, got {len(lines) - 1}."
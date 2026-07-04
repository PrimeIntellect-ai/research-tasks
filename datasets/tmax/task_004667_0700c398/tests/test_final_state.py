# test_final_state.py

import os
import json
import csv
import re
import pytest

INPUT_CSV = "/home/user/data/input.csv"
OUTPUT_DIR = "/home/user/output"
HOURLY_ERRORS_FILE = os.path.join(OUTPUT_DIR, "hourly_errors.json")
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, "checkpoint.json")
SCRIPT_FILE = "/home/user/etl_pipeline.py"

def compute_expected_results():
    if not os.path.exists(INPUT_CSV):
        pytest.fail(f"Input file {INPUT_CSV} is missing.")

    total_logical_rows = 0
    error_rows_found = 0
    extracted_codes_count = 0
    hourly_errors = {}

    code_pattern = re.compile(r"ErrorCode:\s*([A-Z]{3}-\d{4})")

    with open(INPUT_CSV, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)

        for row in reader:
            if not row or len(row) < 3:
                continue
            total_logical_rows += 1
            timestamp, level, message = row[0], row[1], row[2]

            if level == "ERROR":
                error_rows_found += 1
                match = code_pattern.search(message)
                if match:
                    extracted_codes_count += 1
                    code = match.group(1)
                    # Time bucket: YYYY-MM-DDTHH
                    bucket = timestamp[:13]

                    if bucket not in hourly_errors:
                        hourly_errors[bucket] = {}
                    if code not in hourly_errors[bucket]:
                        hourly_errors[bucket][code] = 0
                    hourly_errors[bucket][code] += 1

    return {
        "checkpoint": {
            "total_logical_rows": total_logical_rows,
            "error_rows_found": error_rows_found,
            "extracted_codes_count": extracted_codes_count
        },
        "hourly_errors": hourly_errors
    }

def test_script_exists():
    assert os.path.exists(SCRIPT_FILE), f"The script {SCRIPT_FILE} does not exist."
    assert os.path.isfile(SCRIPT_FILE), f"The path {SCRIPT_FILE} is not a file."

def test_output_files_exist():
    assert os.path.exists(HOURLY_ERRORS_FILE), f"Output file {HOURLY_ERRORS_FILE} does not exist."
    assert os.path.exists(CHECKPOINT_FILE), f"Output file {CHECKPOINT_FILE} does not exist."

def test_checkpoint_contents():
    expected = compute_expected_results()["checkpoint"]

    try:
        with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
            actual = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {CHECKPOINT_FILE} is not valid JSON.")

    for key in ["total_logical_rows", "error_rows_found", "extracted_codes_count"]:
        assert key in actual, f"Key '{key}' is missing from {CHECKPOINT_FILE}."
        assert actual[key] == expected[key], f"Expected {key} to be {expected[key]}, but got {actual[key]}."

def test_hourly_errors_contents():
    expected = compute_expected_results()["hourly_errors"]

    try:
        with open(HOURLY_ERRORS_FILE, 'r', encoding='utf-8') as f:
            actual = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {HOURLY_ERRORS_FILE} is not valid JSON.")

    assert actual == expected, f"Hourly errors JSON does not match expected output.\nExpected: {expected}\nActual: {actual}"
# test_final_state.py

import os
import json
import pytest

OUTPUT_FILE = '/home/user/project/output.json'

def test_output_file_exists():
    """Verify that the output.json file was generated."""
    assert os.path.isfile(OUTPUT_FILE), f"Expected output file {OUTPUT_FILE} is missing. Did the build script run successfully?"

def test_output_file_contents():
    """Verify that the output.json contains the correct year, month, and precision-loss-free total."""
    assert os.path.isfile(OUTPUT_FILE), "Cannot check contents because output.json is missing."

    with open(OUTPUT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{OUTPUT_FILE} is not a valid JSON file.")

    # Check year
    assert "year" in data, "Key 'year' is missing from output.json"
    assert data["year"] == 2023, f"Expected year 2023, but got {data['year']}. The environment variable REPORT_YEAR might still be misconfigured in build.sh."

    # Check month
    assert "month" in data, "Key 'month' is missing from output.json"
    assert data["month"] == 10, f"Expected month 10, but got {data['month']}."

    # Check total
    assert "total" in data, "Key 'total' is missing from output.json"
    actual_total = data["total"]

    # We expect exactly 168.0, not a float with precision loss (e.g. 168.00000000000003)
    # and not a partial sum missing boundary days.
    expected_total = 168.0

    if actual_total < expected_total:
        pytest.fail(f"Expected total {expected_total}, but got {actual_total}. This indicates the SQL query boundary conditions (days 1 and 31) are still missing.")
    elif actual_total != expected_total:
        pytest.fail(f"Expected exact total {expected_total}, but got {actual_total}. Precision loss detected or incorrect row count. Ensure you use math.fsum or Decimal for aggregation.")
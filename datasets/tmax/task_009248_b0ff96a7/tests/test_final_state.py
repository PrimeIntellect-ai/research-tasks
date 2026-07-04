# test_final_state.py

import os
import json
import pytest

def test_ticket_resolution_file():
    filepath = "/home/user/ticket_resolution.txt"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"{filepath} must contain at least two lines."

    line1 = lines[0]
    line2 = lines[1]

    assert "Corrupted input:" in line1, "Line 1 must contain 'Corrupted input:'"
    assert "ERR_CORRUPT_882A" in line1, f"Line 1 should contain the exact corrupted string. Found: {line1}"

    assert "Circular alias IDs:" in line2, "Line 2 must contain 'Circular alias IDs:'"
    assert "10" in line2 and "11" in line2, f"Line 2 should contain the IDs involved in the cycle (10 and 11). Found: {line2}"

def test_export_results_json():
    filepath = "/home/user/export_results.json"
    assert os.path.isfile(filepath), f"File {filepath} does not exist. Did the script run successfully?"

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} is not a valid JSON file.")

    assert isinstance(data, list), "JSON output should be a list of records."

    # Check expected IDs
    expected_ids = {1, 2, 10, 3}
    actual_ids = {record.get("id") for record in data}
    assert expected_ids.issubset(actual_ids), f"Expected records for IDs {expected_ids}, but found {actual_ids}."
    assert len(data) == 4, f"Expected exactly 4 records in the JSON output, but found {len(data)}."

    # Check that cycle detection worked correctly for ID 10
    record_10 = next((r for r in data if r.get("id") == 10), None)
    assert record_10 is not None, "Record for ID 10 is missing."
    assert record_10.get("real_id") == 10, f"For ID 10, real_id should be 10 due to cycle detection. Found: {record_10.get('real_id')}"
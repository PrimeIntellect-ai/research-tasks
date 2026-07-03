# test_final_state.py

import os
import json
import pytest

def test_etl_script_exists():
    """Verify that the ETL script was created."""
    assert os.path.isfile("/home/user/etl.py"), "The ETL script /home/user/etl.py does not exist."

def test_json_output_exists_and_valid():
    """Verify the output JSON file is generated and contains the correct masked data."""
    json_path = "/home/user/clean_data/employees_masked.json"
    assert os.path.isfile(json_path), f"The output file {json_path} does not exist. Did you run your ETL script?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output should be an array (list) of objects."
    assert len(data) == 3, f"Expected 3 records in the JSON output, but found {len(data)}."

    expected_records = [
        {"id": "1", "name": "Alice Smith", "email": "***@company.com", "ssn": "XXX-XX-XXXX"},
        {"id": "2", "name": "Bob Jones", "email": "***@test.org", "ssn": "XXX-XX-XXXX"},
        {"id": "3", "name": "Charlie Brown", "email": "***@domain.net", "ssn": "XXX-XX-XXXX"}
    ]

    # Sort both lists by 'id' to ensure order doesn't cause a failure
    data_sorted = sorted(data, key=lambda x: str(x.get("id", "")))
    expected_sorted = sorted(expected_records, key=lambda x: x["id"])

    for i, (actual, expected) in enumerate(zip(data_sorted, expected_sorted)):
        assert actual.get("id") == expected["id"], f"Record {i} ID mismatch: expected {expected['id']}, got {actual.get('id')}"
        assert actual.get("name") == expected["name"], f"Record {i} Name mismatch: expected {expected['name']}, got {actual.get('name')}"
        assert actual.get("email") == expected["email"], f"Record {i} Email mismatch: expected {expected['email']}, got {actual.get('email')}"
        assert actual.get("ssn") == expected["ssn"], f"Record {i} SSN mismatch: expected {expected['ssn']}, got {actual.get('ssn')}"

def test_cron_configuration():
    """Verify the cron job file is created with the correct schedule and command."""
    cron_path = "/home/user/pipeline.cron"
    assert os.path.isfile(cron_path), f"The cron file {cron_path} does not exist."

    with open(cron_path, "r") as f:
        # Read the file and ignore empty lines
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 1, f"The cron file {cron_path} is empty."

    # The cron expression should be '0 0 * * 0 /usr/bin/python3 /home/user/etl.py'
    # We allow multiple spaces between tokens by splitting and rejoining
    actual_tokens = lines[0].split()
    expected_tokens = "0 0 * * 0 /usr/bin/python3 /home/user/etl.py".split()

    assert actual_tokens == expected_tokens, (
        f"The cron expression in {cron_path} is incorrect. "
        f"Expected: '0 0 * * 0 /usr/bin/python3 /home/user/etl.py', but got: '{lines[0]}'"
    )
# test_final_state.py

import os
import json

def test_backup_report_exists_and_valid():
    report_path = "/home/user/backup_report.json"
    assert os.path.isfile(report_path), f"The output file {report_path} was not created."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    assert isinstance(report_data, list), f"The JSON in {report_path} must be a list (JSON array)."

    expected_data = [
        {
            "region": "eu-west-1",
            "database_name": "auth_db",
            "latest_backup": "2023-10-01T02:00:00Z",
            "total_size_bytes": 10485760
        },
        {
            "region": "eu-west-1",
            "database_name": "inventory_db",
            "latest_backup": "2023-10-01T04:00:00Z",
            "total_size_bytes": 8388608
        },
        {
            "region": "us-east-1",
            "database_name": "payment_db",
            "latest_backup": "2023-10-02T03:00:00Z",
            "total_size_bytes": 105428800
        },
        {
            "region": "us-east-1",
            "database_name": "auth_db",
            "latest_backup": "2023-10-03T02:00:00Z",
            "total_size_bytes": 21485760
        }
    ]

    assert len(report_data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(report_data)}."

    for i, (actual, expected) in enumerate(zip(report_data, expected_data)):
        assert isinstance(actual, dict), f"Record at index {i} is not a JSON object."
        assert actual.get("region") == expected["region"], f"Record {i}: Expected region {expected['region']}, got {actual.get('region')}."
        assert actual.get("database_name") == expected["database_name"], f"Record {i}: Expected database_name {expected['database_name']}, got {actual.get('database_name')}."
        assert actual.get("latest_backup") == expected["latest_backup"], f"Record {i}: Expected latest_backup {expected['latest_backup']}, got {actual.get('latest_backup')}."
        assert actual.get("total_size_bytes") == expected["total_size_bytes"], f"Record {i}: Expected total_size_bytes {expected['total_size_bytes']}, got {actual.get('total_size_bytes')}."

        # Check that there are no extra keys
        assert set(actual.keys()) == set(expected.keys()), f"Record {i} has unexpected keys: {set(actual.keys()) - set(expected.keys())}"
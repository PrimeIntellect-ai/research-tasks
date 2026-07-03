# test_final_state.py

import os
import json
import pytest

def test_c_file_exists():
    """Test that the C source code file was created."""
    assert os.path.isfile("/home/user/config_diff.c"), "/home/user/config_diff.c is missing."

def test_json_report_exists():
    """Test that the JSON report was generated."""
    assert os.path.isfile("/home/user/diff_report.json"), "/home/user/diff_report.json is missing."

def test_json_report_content():
    """Test that the JSON report contains the correct diff data."""
    report_path = "/home/user/diff_report.json"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON.")

    expected_data = [
        {
            "server_id": "srv-101",
            "changes": [
                {
                    "field": "nginx_config",
                    "old_length": 58,
                    "new_length": 62
                },
                {
                    "field": "ssh_keys",
                    "old_length": 30,
                    "new_length": 55
                }
            ]
        },
        {
            "server_id": "srv-201",
            "changes": [
                {
                    "field": "env_vars",
                    "old_length": 20,
                    "new_length": 20
                }
            ]
        },
        {
            "server_id": "srv-202",
            "changes": [
                {
                    "field": "nginx_config",
                    "old_length": 23,
                    "new_length": 28
                }
            ]
        }
    ]

    assert isinstance(data, list), "JSON root should be an array."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} servers with changes, got {len(data)}."

    # Sort both the actual and expected data to ensure order doesn't cause a false failure
    # (though the prompt specifies it should be sorted alphabetically by server_id)
    sorted_data = sorted(data, key=lambda x: x.get("server_id", ""))
    sorted_expected = sorted(expected_data, key=lambda x: x["server_id"])

    for actual_server, expected_server in zip(sorted_data, sorted_expected):
        assert actual_server.get("server_id") == expected_server["server_id"], \
            f"Expected server_id {expected_server['server_id']}, got {actual_server.get('server_id')}."

        actual_changes = sorted(actual_server.get("changes", []), key=lambda x: x.get("field", ""))
        expected_changes = sorted(expected_server["changes"], key=lambda x: x["field"])

        assert actual_changes == expected_changes, \
            f"Changes for server {expected_server['server_id']} do not match. Expected {expected_changes}, got {actual_changes}."
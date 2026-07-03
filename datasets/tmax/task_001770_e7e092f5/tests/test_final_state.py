# test_final_state.py

import os
import json
import pytest

def test_audit_report_json():
    report_path = '/home/user/audit_report.json'

    assert os.path.isfile(report_path), f"The file {report_path} does not exist. Did you run the script?"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert "total_unique_users" in data, "The key 'total_unique_users' is missing from the JSON output."
    assert "shortest_path" in data, "The key 'shortest_path' is missing from the JSON output."

    assert data["total_unique_users"] == 16, f"Expected 16 unique users, but got {data['total_unique_users']}."

    expected_path = ["User_Charlie", "User_Hotel", "User_Zulu"]
    assert data["shortest_path"] == expected_path, f"Expected shortest path {expected_path}, but got {data['shortest_path']}."
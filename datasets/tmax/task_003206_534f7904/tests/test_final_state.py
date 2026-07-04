# test_final_state.py

import os
import json
import pytest

def test_violation_report_exists_and_correct():
    report_path = "/home/user/violation_report.json"
    assert os.path.exists(report_path), f"Violation report not found at {report_path}"

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON in {report_path}: {e}")

    assert "violators" in data, "JSON must contain a 'violators' key at the root level."

    violators = data["violators"]
    assert isinstance(violators, list), "'violators' must be a list."

    expected_violators = [
        {
            "name": "Charlie",
            "role_uri": "http://example.org/role/TempDev"
        },
        {
            "name": "Eve",
            "role_uri": "http://example.org/role/SuperVendor"
        }
    ]

    # Sort the expected list just in case, although it's already sorted
    expected_violators_sorted = sorted(expected_violators, key=lambda x: x["name"])

    # Check that the list has the expected length
    assert len(violators) == len(expected_violators_sorted), f"Expected {len(expected_violators_sorted)} violators, but found {len(violators)}."

    # Check that the list is sorted alphabetically by name
    names = [v.get("name", "") for v in violators]
    assert names == sorted(names), "The violators list must be sorted alphabetically by name."

    # Check exact contents
    for i, expected in enumerate(expected_violators_sorted):
        actual = violators[i]
        assert actual.get("name") == expected["name"], f"Expected violator name '{expected['name']}', got '{actual.get('name')}'"
        assert actual.get("role_uri") == expected["role_uri"], f"Expected role_uri '{expected['role_uri']}' for {expected['name']}, got '{actual.get('role_uri')}'"
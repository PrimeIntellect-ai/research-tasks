# test_final_state.py
import os
import json
import pytest

def test_aggregator_source_exists():
    """Test that the C++ source file exists."""
    assert os.path.isfile("/home/user/aggregator.cpp"), "/home/user/aggregator.cpp is missing. Did you write the source code?"

def test_aggregator_executable_exists():
    """Test that the compiled executable exists."""
    assert os.path.isfile("/home/user/aggregator"), "/home/user/aggregator is missing. Did you compile the program?"
    assert os.access("/home/user/aggregator", os.X_OK), "/home/user/aggregator is not executable."

def test_output_json_exists():
    """Test that the output JSON file exists."""
    assert os.path.isfile("/home/user/output.json"), "/home/user/output.json is missing. Did you run the program?"

def test_output_json_content():
    """Test that the output JSON file contains the correct aggregated data."""
    try:
        with open("/home/user/output.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to parse /home/user/output.json as JSON: {e}")

    assert isinstance(data, list), "Output JSON must be a JSON array."

    expected_data = [
        {
            "manager_id": "U1",
            "department": "Engineering",
            "team_size": 3,
            "combined_roles": ["admin", "deploy", "read", "write"]
        },
        {
            "manager_id": "U4",
            "department": "Marketing",
            "team_size": 2,
            "combined_roles": ["analytics", "content", "social"]
        }
    ]

    # Sort both lists of dicts by manager_id to ensure order
    try:
        data_sorted = sorted(data, key=lambda x: x.get("manager_id", ""))
        expected_sorted = sorted(expected_data, key=lambda x: x["manager_id"])
    except Exception as e:
        pytest.fail(f"Output JSON is missing expected keys or has invalid structure: {e}")

    assert len(data_sorted) == len(expected_sorted), f"Expected {len(expected_sorted)} managers in output, got {len(data_sorted)}"

    for actual, expected in zip(data_sorted, expected_sorted):
        assert actual.get("manager_id") == expected["manager_id"], f"Expected manager_id {expected['manager_id']}, got {actual.get('manager_id')}"
        assert actual.get("department") == expected["department"], f"Expected department {expected['department']} for {expected['manager_id']}, got {actual.get('department')}"
        assert actual.get("team_size") == expected["team_size"], f"Expected team_size {expected['team_size']} for {expected['manager_id']}, got {actual.get('team_size')}"

        actual_roles = actual.get("combined_roles", [])
        assert isinstance(actual_roles, list), f"combined_roles must be a list for {expected['manager_id']}"
        assert sorted(actual_roles) == sorted(expected["combined_roles"]), f"Expected combined_roles {expected['combined_roles']} for {expected['manager_id']}, got {actual_roles}"
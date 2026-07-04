# test_final_state.py
import os
import json
import pytest

def test_report_json_exists_and_content():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected JSON root to be a list, got {type(data).__name__}."
    assert len(data) == 2, f"Expected 2 entries in the JSON array, got {len(data)}."

    expected_data = [
        {
            "database_name": "auth_db",
            "latest_backup_time": "2023-10-04 10:00:00",
            "latest_size_bytes": 1100,
            "size_diff_from_previous": 50
        },
        {
            "database_name": "payments_db",
            "latest_backup_time": "2023-10-02 11:00:00",
            "latest_size_bytes": 4800,
            "size_diff_from_previous": -200
        }
    ]

    # Sort both just in case, though the instructions say sort alphabetically by database_name
    data_sorted = sorted(data, key=lambda x: x.get("database_name", ""))
    expected_sorted = sorted(expected_data, key=lambda x: x["database_name"])

    for i, (actual, expected) in enumerate(zip(data_sorted, expected_sorted)):
        assert actual.get("database_name") == expected["database_name"], f"Mismatch in database_name at index {i}"
        assert actual.get("latest_backup_time") == expected["latest_backup_time"], f"Mismatch in latest_backup_time at index {i}"
        assert actual.get("latest_size_bytes") == expected["latest_size_bytes"], f"Mismatch in latest_size_bytes at index {i}"
        assert actual.get("size_diff_from_previous") == expected["size_diff_from_previous"], f"Mismatch in size_diff_from_previous at index {i}"

def test_analyze_go_requirements():
    go_path = "/home/user/analyze.go"
    assert os.path.exists(go_path), f"Go source file {go_path} does not exist."
    assert os.path.isfile(go_path), f"{go_path} is not a file."

    with open(go_path, "r") as f:
        content = f.read()

    # Check for parameterized queries
    # Look for common parameter placeholders in Go's database/sql (?, $1, @param)
    has_placeholder = "?" in content or "$1" in content or "@" in content
    assert has_placeholder, "The Go program does not appear to use parameterized queries (e.g., '?' or '$1')."

    # Check for LAG window function
    assert "LAG" in content.upper(), "The Go program does not appear to use the 'LAG' window function."
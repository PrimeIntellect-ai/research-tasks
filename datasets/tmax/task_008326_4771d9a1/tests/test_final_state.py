# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/compliance.db"
REPORT_PATH = "/home/user/audit_report.json"

def test_database_indexes():
    """Verify that the old index is dropped and the new index is created correctly."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check that the old index is dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_employee_assets';")
    old_index = cursor.fetchone()
    assert old_index is None, "The index 'idx_employee_assets' was not dropped."

    # Check that the new index exists
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND name='idx_assets_emp_val';")
    new_index = cursor.fetchone()
    assert new_index is not None, "The index 'idx_assets_emp_val' was not created."

    # Optionally, verify the index definition (e.g., columns and order)
    sql = new_index[1].lower()
    assert "employee_id" in sql, "The new index must cover 'employee_id'."
    assert "value" in sql, "The new index must cover 'value'."
    assert "desc" in sql, "The new index must sort 'value' in DESC order."

    conn.close()

def test_json_report():
    """Verify the generated JSON report exists and contains the correct data."""
    assert os.path.exists(REPORT_PATH), f"Report file missing at {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file audit_report.json is not valid JSON.")

    expected_data = [
        {"employee_id": 2, "name": "Bob", "total_asset_value": 6000, "asset_count": 2},
        {"employee_id": 6, "name": "Frank", "total_asset_value": 2500, "asset_count": 2},
        {"employee_id": 1, "name": "Alice", "total_asset_value": 2000, "asset_count": 1},
        {"employee_id": 3, "name": "Charlie", "total_asset_value": 1500, "asset_count": 1},
        {"employee_id": 4, "name": "Diana", "total_asset_value": 500, "asset_count": 1},
        {"employee_id": 5, "name": "Eve", "total_asset_value": 0, "asset_count": 0}
    ]

    assert isinstance(report_data, list), "The JSON report must be a list of objects."
    assert len(report_data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(report_data)}."

    for i, (actual, expected) in enumerate(zip(report_data, expected_data)):
        assert actual.get("employee_id") == expected["employee_id"], f"Record {i}: expected employee_id {expected['employee_id']}, got {actual.get('employee_id')}"
        assert actual.get("name") == expected["name"], f"Record {i}: expected name '{expected['name']}', got '{actual.get('name')}'"
        assert actual.get("total_asset_value") == expected["total_asset_value"], f"Record {i}: expected total_asset_value {expected['total_asset_value']}, got {actual.get('total_asset_value')}"
        assert actual.get("asset_count") == expected["asset_count"], f"Record {i}: expected asset_count {expected['asset_count']}, got {actual.get('asset_count')}"
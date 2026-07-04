# test_final_state.py
import os
import json
import sqlite3
import re
import pytest

DB_PATH = '/home/user/analytics.db'
SQL_PATH = '/home/user/optimize.sql'
PY_PATH = '/home/user/fast_report.py'
JSON_PATH = '/home/user/report_output.json'

def test_optimize_sql_exists_and_contains_indexes():
    assert os.path.exists(SQL_PATH), f"{SQL_PATH} does not exist."
    with open(SQL_PATH, 'r') as f:
        content = f.read().upper()
    assert "CREATE INDEX" in content, f"{SQL_PATH} does not contain CREATE INDEX statements."

def test_db_has_indexes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
    indexes = c.fetchall()
    conn.close()

    indexed_tables = [row[1] for row in indexes]
    assert 'users' in indexed_tables, "No index found on 'users' table."
    assert 'sessions' in indexed_tables, "No index found on 'sessions' table."
    assert 'events' in indexed_tables, "No index found on 'events' table."

def test_python_script_uses_parameterized_queries():
    assert os.path.exists(PY_PATH), f"{PY_PATH} does not exist."
    with open(PY_PATH, 'r') as f:
        content = f.read()

    # Check for parameterized queries (either ? or named parameters like :tenant)
    has_param_marker = re.search(r'\?|:\w+', content)
    assert has_param_marker is not None, "The script does not appear to use parameterized queries (? or :name)."

def test_report_output_json():
    assert os.path.exists(JSON_PATH), f"{JSON_PATH} does not exist."
    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{JSON_PATH} is not valid JSON.")

    expected_data = [
        {"user_id": 139, "name": "User_139", "total_purchase_value": 1599.25},
        {"user_id": 997, "name": "User_997", "total_purchase_value": 1345.54},
        {"user_id": 483, "name": "User_483", "total_purchase_value": 1058.46},
        {"user_id": 923, "name": "User_923", "total_purchase_value": 624.93},
        {"user_id": 12,  "name": "User_12",  "total_purchase_value": 381.16}
    ]

    assert isinstance(data, list), "Output JSON must be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get("user_id") == expected["user_id"], f"Record {i}: Expected user_id {expected['user_id']}, got {actual.get('user_id')}"
        assert actual.get("name") == expected["name"], f"Record {i}: Expected name '{expected['name']}', got '{actual.get('name')}'"

        actual_val = actual.get("total_purchase_value")
        assert actual_val is not None, f"Record {i}: Missing 'total_purchase_value'"
        assert abs(actual_val - expected["total_purchase_value"]) < 0.01, f"Record {i}: Expected total_purchase_value {expected['total_purchase_value']}, got {actual_val}"
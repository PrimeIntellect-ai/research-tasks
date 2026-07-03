# test_final_state.py
import os
import json
import sqlite3
import pytest

FIXED_QUERY_PATH = "/home/user/fixed_query.sql"
AUDIT_SUMMARY_PATH = "/home/user/audit_summary.json"
DB_PATH = "/home/user/compliance.db"

def test_fixed_query_exists_and_correct():
    assert os.path.exists(FIXED_QUERY_PATH), f"Fixed query file missing at {FIXED_QUERY_PATH}"
    assert os.path.isfile(FIXED_QUERY_PATH), f"{FIXED_QUERY_PATH} is not a file"

    with open(FIXED_QUERY_PATH, 'r') as f:
        query = f.read().strip()

    assert query, "Fixed query file is empty"

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Executing fixed_query.sql failed with error: {e}")
    finally:
        conn.close()

    # Verify columns
    if rows:
        columns = [description[0].lower() for description in cursor.description]
        assert "name" in columns and "total_sent" in columns, \
            f"Query must return 'name' and 'total_sent' columns. Got: {columns}"

    # Verify results
    results_dict = {row["name"]: row["total_sent"] for row in rows}
    expected_results = {
        "Alice": 350,
        "Charlie": 600
    }

    assert results_dict == expected_results, \
        f"Query results are incorrect. Expected {expected_results}, got {results_dict}"

def test_audit_summary_json():
    assert os.path.exists(AUDIT_SUMMARY_PATH), f"Audit summary file missing at {AUDIT_SUMMARY_PATH}"
    assert os.path.isfile(AUDIT_SUMMARY_PATH), f"{AUDIT_SUMMARY_PATH} is not a file"

    try:
        with open(AUDIT_SUMMARY_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"File {AUDIT_SUMMARY_PATH} is not valid JSON: {e}")

    assert isinstance(data, dict), f"JSON content must be a dictionary, got {type(data)}"

    assert "highest_transfer_employee" in data, "Missing key 'highest_transfer_employee' in JSON"
    assert data["highest_transfer_employee"] == "Charlie", \
        f"Incorrect highest_transfer_employee. Expected 'Charlie', got {data['highest_transfer_employee']}"

    assert "central_trader_id" in data, "Missing key 'central_trader_id' in JSON"
    assert data["central_trader_id"] == 5, \
        f"Incorrect central_trader_id. Expected 5, got {data['central_trader_id']}"
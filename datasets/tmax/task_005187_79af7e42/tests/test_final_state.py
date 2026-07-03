# test_final_state.py

import os
import sqlite3
import json
import pytest

def test_c_source_and_executable_exist():
    assert os.path.isfile("/home/user/audit.c"), "The C source file /home/user/audit.c is missing."
    assert os.path.isfile("/home/user/audit_tool"), "The compiled executable /home/user/audit_tool is missing."
    assert os.access("/home/user/audit_tool", os.X_OK), "The file /home/user/audit_tool is not executable."

def test_violations_json_exists_and_valid():
    json_path = "/home/user/violations.json"
    assert os.path.isfile(json_path), f"The output file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output must be a top-level array."

def test_violations_json_content():
    db_path = "/home/user/audit.db"
    json_path = "/home/user/violations.json"

    if not os.path.isfile(db_path):
        pytest.fail(f"Database {db_path} is missing, cannot compute expected results.")

    if not os.path.isfile(json_path):
        pytest.fail(f"JSON file {json_path} is missing.")

    # Compute expected results from the database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    WITH paths AS (
      SELECT u1.id as source_user, u2.id as target_user,
             (u1.risk_weight + r1.risk_weight + r2.risk_weight + u2.risk_weight) as path_risk,
             ROW_NUMBER() OVER(PARTITION BY u2.id ORDER BY (u1.risk_weight + r1.risk_weight + r2.risk_weight + u2.risk_weight) DESC, u1.id ASC) as rn
      FROM nodes u1
      JOIN edges e1 ON u1.id = e1.src AND e1.rel_type = 'ASSUMES'
      JOIN nodes r1 ON e1.dst = r1.id AND r1.type = 'ROLE'
      JOIN edges e2 ON r1.id = e2.src AND e2.rel_type = 'INHERITS'
      JOIN nodes r2 ON e2.dst = r2.id AND r2.type = 'ROLE'
      JOIN edges e3 ON r2.id = e3.src AND e3.rel_type = 'CAN_MODIFY'
      JOIN nodes u2 ON e3.dst = u2.id AND u2.type = 'USER'
      WHERE u1.type = 'USER' AND u1.id != u2.id
    )
    SELECT target_user, source_user, path_risk FROM paths WHERE rn = 1 ORDER BY target_user ASC;
    """

    try:
        cursor.execute(query)
        expected_rows = cursor.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to query database for expected results: {e}")
    finally:
        conn.close()

    expected_data = [
        {
            "target_user": row["target_user"],
            "source_user": row["source_user"],
            "path_risk": row["path_risk"]
        }
        for row in expected_rows
    ]

    with open(json_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert actual_data == expected_data, f"The content of {json_path} does not match the expected output. Expected: {expected_data}, Actual: {actual_data}"
# test_final_state.py
import os
import json
import sqlite3
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_bom.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_db_and_table_exists():
    db_path = "/home/user/bom.db"
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='parts'")
    table = cursor.fetchone()
    conn.close()

    assert table is not None, "Table 'parts' does not exist in the database."

def test_index_exists():
    db_path = "/home/user/bom.db"
    assert os.path.exists(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='parts'")
    indices = cursor.fetchall()

    index_on_parent_id = False
    for (idx_name,) in indices:
        if idx_name.startswith("sqlite_autoindex"):
            continue
        cursor.execute(f"PRAGMA index_info({idx_name})")
        columns = cursor.fetchall()
        # Check if the first column in the index is parent_id
        if columns and columns[0][2] == "parent_id":
            index_on_parent_id = True
            break

    conn.close()
    assert index_on_parent_id, "No index on 'parent_id' found for the 'parts' table."

def test_query_plan_uses_index():
    plan_path = "/home/user/query_plan.txt"
    assert os.path.exists(plan_path), f"Query plan file {plan_path} does not exist."

    with open(plan_path, "r") as f:
        content = f.read().upper()

    assert "USING INDEX" in content or "USING COVERING INDEX" in content, \
        "The query plan does not indicate that an index was used (missing 'USING INDEX')."

def test_json_output_correct():
    json_path = "/home/user/top_parts.json"
    assert os.path.exists(json_path), f"JSON output file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected = [
      {"id": 1, "name": "Engine", "depth": 0, "cost": 5000.0, "cost_rank": 1},
      {"id": 7, "name": "Chassis", "depth": 0, "cost": 2000.0, "cost_rank": 2},
      {"id": 8, "name": "Frame", "depth": 1, "cost": 1500.0, "cost_rank": 1},
      {"id": 9, "name": "Suspension", "depth": 1, "cost": 400.0, "cost_rank": 2},
      {"id": 10, "name": "Shock Absorber", "depth": 2, "cost": 120.0, "cost_rank": 1},
      {"id": 6, "name": "Connecting Rod", "depth": 2, "cost": 80.0, "cost_rank": 2}
    ]

    assert isinstance(data, list), "JSON output should be a list of objects."
    assert len(data) == len(expected), f"Expected {len(expected)} records, but got {len(data)}."

    for i, (actual_row, expected_row) in enumerate(zip(data, expected)):
        # Normalize keys and values for comparison
        actual_normalized = {k.lower(): v for k, v in actual_row.items()}
        for key, exp_val in expected_row.items():
            assert key in actual_normalized, f"Row {i} is missing key '{key}'"
            if isinstance(exp_val, float):
                assert abs(float(actual_normalized[key]) - exp_val) < 1e-5, f"Row {i} key '{key}' mismatch: expected {exp_val}, got {actual_normalized[key]}"
            else:
                assert actual_normalized[key] == exp_val, f"Row {i} key '{key}' mismatch: expected {exp_val}, got {actual_normalized[key]}"
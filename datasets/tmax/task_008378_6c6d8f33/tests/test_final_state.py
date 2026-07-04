# test_final_state.py

import os
import json
import sqlite3
import pytest
import configparser

REPO_DIR = "/home/user/numsock_repo"
DB_PATH = os.path.join(REPO_DIR, "data.db")
FINAL_RESULT_PATH = "/home/user/final_result.json"
PYPROJECT_PATH = os.path.join(REPO_DIR, "pyproject.toml")

def test_pyproject_toml_fixed():
    """Verify that pyproject.toml is syntactically valid and contains websockets."""
    assert os.path.isfile(PYPROJECT_PATH), "pyproject.toml is missing."
    with open(PYPROJECT_PATH, "r") as f:
        content = f.read()

    # Check that the quote is fixed
    assert 'name = "numsock"' in content or "name = 'numsock'" in content, "The 'name' field in pyproject.toml is still broken."

    # Check for websockets dependency
    assert "websockets" in content, "The 'websockets' dependency is missing from pyproject.toml."

def test_database_schema_and_contents():
    """Verify that the SQLite database has the correct schema and data."""
    assert os.path.isfile(DB_PATH), "data.db is missing. The server might not have run or initialized the DB."

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Check schema
    c.execute("PRAGMA table_info(records)")
    columns = {row["name"]: row["type"].upper() for row in c.fetchall()}

    assert "ema" in columns, "The 'ema' column is missing from the 'records' table."
    assert "FLOATX" not in columns.get("ema", ""), "The 'ema' column has the invalid type 'FLOATX'."

    # Check contents
    c.execute("SELECT id, value, ema FROM records ORDER BY id ASC")
    rows = c.fetchall()

    assert len(rows) >= 3, "The database does not contain the expected number of records."

    # Check the first three records based on test_client.py
    expected_values = [10.0, 20.0, 15.0]

    # Calculate expected EMAs
    expected_emas = []
    alpha = 0.5
    last_ema = None
    for v in expected_values:
        if last_ema is None:
            last_ema = v
        else:
            last_ema = (v * alpha) + (last_ema * (1 - alpha))
        expected_emas.append(last_ema)

    for i in range(3):
        assert float(rows[i]["value"]) == expected_values[i], f"Record {i+1} value mismatch."
        assert float(rows[i]["ema"]) == expected_emas[i], f"Record {i+1} ema mismatch."

    conn.close()

def test_final_result_json():
    """Verify that final_result.json matches the expected output."""
    assert os.path.isfile(FINAL_RESULT_PATH), "final_result.json is missing."

    with open(FINAL_RESULT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("final_result.json does not contain valid JSON.")

    assert isinstance(data, list), "final_result.json must contain a JSON array."
    assert len(data) >= 3, "final_result.json does not contain enough records."

    expected_values = [10.0, 20.0, 15.0]
    expected_emas = [10.0, 15.0, 15.0]

    for i in range(3):
        row = data[i]
        assert "id" in row and "value" in row and "ema" in row, f"Row {i+1} is missing required keys."
        assert float(row["value"]) == expected_values[i], f"JSON Row {i+1} value mismatch."
        assert float(row["ema"]) == expected_emas[i], f"JSON Row {i+1} ema mismatch."
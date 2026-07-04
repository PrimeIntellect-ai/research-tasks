# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = '/home/user/graph.db'
INDEXES_SQL_PATH = '/home/user/indexes.sql'
PIPELINE_PY_PATH = '/home/user/etl_pipeline.py'
JSON_OUT_PATH = '/home/user/optimized_chains.json'

def test_indexes_sql_exists_and_valid():
    """Verify indexes.sql exists and contains CREATE INDEX statements."""
    assert os.path.exists(INDEXES_SQL_PATH), f"{INDEXES_SQL_PATH} does not exist."
    with open(INDEXES_SQL_PATH, 'r') as f:
        content = f.read().upper()
    assert "CREATE INDEX" in content, f"{INDEXES_SQL_PATH} must contain CREATE INDEX statements."

def test_database_has_indexes():
    """Verify that indexes were actually created in the SQLite database."""
    assert os.path.exists(DB_PATH), f"{DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = c.fetchall()
    conn.close()
    assert len(indexes) > 0, "No custom indexes found in the database. Did you execute the SQL script?"

def test_pipeline_script_exists():
    """Verify etl_pipeline.py exists."""
    assert os.path.exists(PIPELINE_PY_PATH), f"{PIPELINE_PY_PATH} does not exist."

def test_optimized_chains_json():
    """Verify the JSON output matches the expected optimal supply chains."""
    assert os.path.exists(JSON_OUT_PATH), f"{JSON_OUT_PATH} does not exist."

    with open(JSON_OUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{JSON_OUT_PATH} is not valid JSON.")

    assert isinstance(data, list), f"JSON root must be an array, got {type(data)}."

    expected_data = [
        {
            "manufacturer": "M1",
            "supplier": "S2",
            "retailer": "R1",
            "total_cost": 7.0
        },
        {
            "manufacturer": "M2",
            "supplier": "S1",
            "retailer": "R2",
            "total_cost": 12.0
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not an object."
        assert actual.get("manufacturer") == expected["manufacturer"], f"Mismatch in manufacturer at index {i}."
        assert actual.get("supplier") == expected["supplier"], f"Mismatch in supplier at index {i}."
        assert actual.get("retailer") == expected["retailer"], f"Mismatch in retailer at index {i}."
        assert actual.get("total_cost") == expected["total_cost"], f"Mismatch in total_cost at index {i}."
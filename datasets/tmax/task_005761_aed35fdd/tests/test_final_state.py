# test_final_state.py

import os
import json
import sqlite3
import pytest

JSON_PATH = '/home/user/schema_hops.json'
SQL_PATH = '/home/user/optimize.sql'
DB_PATH = '/home/user/ecommerce.db'

def test_schema_hops_json():
    """Test that schema_hops.json exists and contains the correct data."""
    assert os.path.exists(JSON_PATH), f"File missing at {JSON_PATH}"

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert "1_hop" in data, "Missing '1_hop' key in JSON"
    assert "2_hops" in data, "Missing '2_hops' key in JSON"

    assert isinstance(data["1_hop"], list), "'1_hop' must be a list"
    assert isinstance(data["2_hops"], list), "'2_hops' must be a list"

    assert sorted(data["1_hop"]) == ["orders", "reviews"], "1_hop list is incorrect"
    assert sorted(data["2_hops"]) == ["order_items"], "2_hops list is incorrect"

def test_optimize_sql():
    """Test that optimize.sql exists, contains the correct statement, and creates the correct index."""
    assert os.path.exists(SQL_PATH), f"File missing at {SQL_PATH}"

    with open(SQL_PATH, 'r') as f:
        sql = f.read().strip()

    assert "CREATE INDEX" in sql.upper(), "Missing CREATE INDEX statement"
    assert "idx_orders_etl" in sql, "Index name 'idx_orders_etl' is missing or incorrect"

    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(sql)
    except sqlite3.Error as e:
        pytest.fail(f"Executing optimize.sql failed with error: {e}")

    cursor = conn.cursor()
    cursor.execute("PRAGMA index_info(idx_orders_etl)")
    cols = [row[2] for row in cursor.fetchall()]

    assert cols, "Index 'idx_orders_etl' was not created properly or has no columns."
    assert cols[0] == 'status', "Equality filter 'status' should be the first column in the index."
    assert set(cols) == {'status', 'created_at', 'user_id'}, "Index does not cover the correct columns (status, created_at, user_id)."

    conn.close()
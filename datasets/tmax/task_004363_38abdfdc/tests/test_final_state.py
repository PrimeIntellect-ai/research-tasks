# test_final_state.py
import os
import sqlite3
import json
import pytest

def test_index_created():
    db_path = "/home/user/sales.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_sales_perf';")
    index = cursor.fetchone()
    conn.close()

    assert index is not None, "Index 'idx_sales_perf' was not created in the database."
    assert index[0] == 'idx_sales_perf', "Index name mismatch."

def test_json_output():
    json_path = "/home/user/top_sales.json"
    assert os.path.exists(json_path), f"JSON output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected = [
        {"region": "North", "salesperson": "Alice", "total_sales": 5000.5, "region_total": 12500.5, "rank": 1},
        {"region": "North", "salesperson": "Diana", "total_sales": 4000.0, "region_total": 12500.5, "rank": 2},
        {"region": "South", "salesperson": "Eve", "total_sales": 7000.0, "region_total": 11500.0, "rank": 1},
        {"region": "South", "salesperson": "Grace", "total_sales": 2500.0, "region_total": 11500.0, "rank": 2}
    ]

    assert isinstance(data, list), "JSON root should be a list of objects."
    assert len(data) == len(expected), f"Expected {len(expected)} elements in JSON, found {len(data)}."

    for i, (actual_item, expected_item) in enumerate(zip(data, expected)):
        assert actual_item == expected_item, f"Mismatch at index {i}. Expected {expected_item}, got {actual_item}."
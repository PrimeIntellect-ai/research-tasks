# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_index_dropped():
    db_path = "/home/user/data.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND name='idx_active';")
    count = cursor.fetchone()[0]
    conn.close()

    assert count == 0, "The index 'idx_active' was not dropped from the database."

def test_summary_json_content():
    summary_path = "/home/user/summary.json"
    assert os.path.isfile(summary_path), f"Output file {summary_path} is missing."

    with open(summary_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{summary_path} is not a valid JSON file.")

    expected_data = [
        {"dept_id": 1, "total_sales": 160},
        {"dept_id": 2, "total_sales": 120},
        {"dept_id": 3, "total_sales": 30},
        {"dept_id": 4, "total_sales": 100},
        {"dept_id": 6, "total_sales": 60}
    ]

    assert isinstance(data, list), f"{summary_path} should contain a JSON array."
    assert data == expected_data, f"The contents of {summary_path} do not match the expected output. Got: {data}"
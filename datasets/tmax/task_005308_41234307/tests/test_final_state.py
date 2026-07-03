# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_json_output():
    json_path = '/home/user/lineage_1.json'
    assert os.path.exists(json_path), f"Output file {json_path} does not exist. Did you run the script and redirect the output?"
    assert os.path.isfile(json_path), f"Path {json_path} is not a regular file."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(data, list), "JSON output must be an array of objects."

    ids = {row.get('id') for row in data}
    expected_ids = {1, 2, 3, 4}
    assert ids == expected_ids, f"Expected the JSON output to contain backup IDs {expected_ids}, but got {ids}. The recursive CTE might still be incorrect."

def test_database_index():
    db_path = '/home/user/backups.db'
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_parent';")
    index = cursor.fetchone()
    conn.close()

    assert index is not None, "Index 'idx_parent' was not found in the database. Did you add the CREATE INDEX command to the Python script?"
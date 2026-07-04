# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/org.db"
JSON_PATH = "/home/user/deep_org.json"

def test_database_exists():
    assert os.path.isfile(DB_PATH), f"The database file {DB_PATH} does not exist."

def test_index_exists():
    assert os.path.isfile(DB_PATH), f"The database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_manager';")
    result = cursor.fetchone()

    conn.close()

    assert result is not None, "The index 'idx_manager' does not exist in the database."
    assert result[0] == 'idx_manager', "The index 'idx_manager' was not found."

def test_json_export_exists():
    assert os.path.isfile(JSON_PATH), f"The JSON file {JSON_PATH} does not exist."

def test_json_export_content():
    assert os.path.isfile(JSON_PATH), f"The JSON file {JSON_PATH} does not exist."

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {JSON_PATH} does not contain valid JSON.")

    expected_data = [
        {"id": 7, "path": "1->2->4->7"},
        {"id": 8, "path": "1->2->5->8"},
        {"id": 9, "path": "1->2->5->8->9"}
    ]

    assert isinstance(data, list), "The JSON data should be a list of objects."

    # Sort both lists by id just in case, though the prompt requires them to be sorted.
    data_sorted = sorted(data, key=lambda x: x.get("id", 0))
    expected_sorted = sorted(expected_data, key=lambda x: x["id"])

    assert data_sorted == expected_sorted, f"The content of {JSON_PATH} does not match the expected output."
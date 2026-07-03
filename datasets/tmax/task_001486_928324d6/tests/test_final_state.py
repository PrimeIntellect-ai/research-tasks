# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/kg.db'
RESULT_PATH = '/home/user/result.json'

def test_result_file_exists():
    assert os.path.exists(RESULT_PATH), f"The file {RESULT_PATH} was not created."
    assert os.path.isfile(RESULT_PATH), f"{RESULT_PATH} is not a valid file."

def test_result_file_content():
    with open(RESULT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {RESULT_PATH} does not contain valid JSON.")

    expected = ["AlphaBot", "Omni_Agent", "Zeta_System"]

    assert isinstance(data, list), f"Expected a JSON array, but got {type(data).__name__}."
    assert data == expected, f"Expected {expected}, but got {data}."

def test_index_created():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND tbl_name='triples';")
    count = cursor.fetchone()[0]
    conn.close()

    assert count >= 1, "No index was created on the 'triples' table. You must optimize the query by creating at least one index."

def test_data_not_modified():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM triples;")
    count = cursor.fetchone()[0]
    conn.close()

    assert count >= 100000, "The data in the 'triples' table appears to have been modified or deleted. Expected at least 100,000 rows."
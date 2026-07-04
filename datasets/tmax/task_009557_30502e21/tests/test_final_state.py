# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = '/home/user/social_network.db'
PATH_TXT = '/home/user/path.txt'
PATH_PROFILES = '/home/user/path_profiles.json'

def test_indexes_optimized():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check that only idx_cover exists on connections
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='connections';")
    indexes = {row[0] for row in cursor.fetchall()}

    assert 'idx_cover' in indexes, "Index 'idx_cover' was not created."
    assert len(indexes) == 1, f"Expected only 'idx_cover' on connections table, but found: {indexes}"

    # Check columns in idx_cover
    cursor.execute("PRAGMA index_info('idx_cover');")
    columns = [row[2] for row in cursor.fetchall()]

    assert len(columns) == 3, f"Index 'idx_cover' should cover 3 columns, but covers {len(columns)}."
    assert columns[0] == 'user_id', f"First column of 'idx_cover' must be 'user_id' for efficient filtering, found '{columns[0]}'."
    assert set(columns) == {'user_id', 'friend_id', 'interaction_score'}, f"Index 'idx_cover' does not cover the correct columns. Found: {columns}"

    conn.close()

def test_path_txt_output():
    assert os.path.isfile(PATH_TXT), f"Output file {PATH_TXT} is missing."

    with open(PATH_TXT, 'r') as f:
        content = f.read().strip()

    assert content == '10,88,42', f"Expected path '10,88,42', but got '{content}'."

def test_path_profiles_json_output():
    assert os.path.isfile(PATH_PROFILES), f"Output file {PATH_PROFILES} is missing."

    with open(PATH_PROFILES, 'r') as f:
        try:
            profiles = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {PATH_PROFILES} does not contain valid JSON.")

    expected_profiles = [
        {"name": "User 10", "age": 20, "path_order": 0},
        {"name": "User 88", "age": 28, "path_order": 1},
        {"name": "User 42", "age": 22, "path_order": 2}
    ]

    assert profiles == expected_profiles, f"JSON profiles do not match expected output.\nExpected: {expected_profiles}\nGot: {profiles}"
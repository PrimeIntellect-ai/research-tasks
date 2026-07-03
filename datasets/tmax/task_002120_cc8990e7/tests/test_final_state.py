# test_final_state.py
import os
import sqlite3
import pytest

REACH_FILE = '/home/user/reach.txt'
SQL_FILE = '/home/user/indexes.sql'
DB_PATH = '/home/user/network.db'

def test_reach_value():
    assert os.path.exists(REACH_FILE), f"The file {REACH_FILE} does not exist."
    with open(REACH_FILE, 'r') as f:
        content = f.read().strip()

    try:
        reach_val = float(content)
    except ValueError:
        pytest.fail(f"The content of {REACH_FILE} could not be parsed as a float. Found: '{content}'")

    assert reach_val == 4.5, f"Expected Extended Reach to be 4.5, but got {reach_val}."

def test_sql_file_exists_and_contains_create_index():
    assert os.path.exists(SQL_FILE), f"The file {SQL_FILE} does not exist."
    with open(SQL_FILE, 'r') as f:
        content = f.read().lower()

    assert "create " in content and "index " in content, f"{SQL_FILE} does not seem to contain CREATE INDEX statements."
    assert "follows" in content, f"{SQL_FILE} does not seem to reference the 'follows' table."

def test_database_has_new_indexes():
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query for user-created indexes on the 'follows' table
    cursor.execute("""
        SELECT name, sql 
        FROM sqlite_master 
        WHERE type='index' 
          AND tbl_name='follows' 
          AND sql IS NOT NULL
    """)
    indexes = cursor.fetchall()

    # Filter out auto-indexes just in case, though they usually have sql IS NULL or start with sqlite_autoindex
    user_created_indexes = [idx for idx in indexes if not idx[0].startswith('sqlite_autoindex_')]

    assert len(user_created_indexes) > 0, "No new user-created indexes found on the 'follows' table in the database."

    conn.close()
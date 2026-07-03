# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/valid_translations.db"

def test_db_exists():
    assert os.path.isfile(DB_PATH), f"The database file {DB_PATH} was not created."

def test_db_schema():
    assert os.path.isfile(DB_PATH), f"Database {DB_PATH} not found."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='translations';")
    table_exists = cursor.fetchone()
    assert table_exists is not None, "Table 'translations' does not exist in the database."

    cursor.execute("PRAGMA table_info(translations);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    assert "id" in columns, "Column 'id' missing from translations table."
    assert "english" in columns, "Column 'english' missing from translations table."
    assert "translated" in columns, "Column 'translated' missing from translations table."
    assert "distance" in columns, "Column 'distance' missing from translations table."

    conn.close()

def test_db_contents():
    assert os.path.isfile(DB_PATH), f"Database {DB_PATH} not found."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, distance FROM translations ORDER BY id;")
    rows = cursor.fetchall()

    expected_rows = {
        "row1": 13,
        "row3": 8,
        "row5": 10,
        "row7": 33
    }

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in the database, found {len(rows)}."

    for row_id, distance in rows:
        assert row_id in expected_rows, f"Unexpected row '{row_id}' found in the database."
        expected_distance = expected_rows[row_id]
        assert distance == expected_distance, f"Expected distance {expected_distance} for {row_id}, but got {distance}."

    conn.close()
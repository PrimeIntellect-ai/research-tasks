# test_final_state.py

import os
import json
import sqlite3
import pytest

APP_DIR = "/home/user/app"
SO_FILE = os.path.join(APP_DIR, "libuserhash.so")
DB_FILE = os.path.join(APP_DIR, "data.db")
RESULT_JSON = "/home/user/result.json"

def test_shared_library_exists():
    assert os.path.isfile(SO_FILE), f"Shared library {SO_FILE} does not exist."
    with open(SO_FILE, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{SO_FILE} is not a valid ELF file."

def test_database_schema_and_data():
    assert os.path.isfile(DB_FILE), f"Database file {DB_FILE} does not exist."

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees';")
    table = cursor.fetchone()
    assert table is not None, "Table 'employees' does not exist in the database."

    cursor.execute("PRAGMA table_info(employees);")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = {"id": "INTEGER", "first_name": "TEXT", "last_name": "TEXT", "age_years": "INTEGER"}

    for col_name, col_type in expected_columns.items():
        assert col_name in columns, f"Column '{col_name}' is missing from 'employees' table."
        # SQLite types can be loosely typed, but we check if the declared type contains the expected string
        assert col_type in columns[col_name], f"Column '{col_name}' should be of type {col_type}."

    assert "full_name" not in columns, "Column 'full_name' should have been dropped."
    assert "age" not in columns, "Column 'age' should have been dropped/renamed."

    # Check data migration
    cursor.execute("SELECT id, first_name, last_name, age_years FROM employees ORDER BY id;")
    rows = cursor.fetchall()

    assert len(rows) == 2, f"Expected 2 rows in 'employees' table, found {len(rows)}."

    assert rows[0] == (1, 'Alice', 'Smith', 30), f"First row data mismatch: {rows[0]}"
    assert rows[1] == (2, 'Bob', 'Jones', 45), f"Second row data mismatch: {rows[1]}"

    conn.close()

def test_result_json():
    assert os.path.isfile(RESULT_JSON), f"Result file {RESULT_JSON} does not exist."

    with open(RESULT_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULT_JSON} does not contain valid JSON.")

    expected_data = {
        "id": 1,
        "first_name": "Alice",
        "last_name": "Smith",
        "age_years": 30,
        "hash": 7
    }

    for key, value in expected_data.items():
        assert key in data, f"Key '{key}' missing from JSON response."
        assert data[key] == value, f"Value for '{key}' is incorrect. Expected {value}, got {data[key]}."
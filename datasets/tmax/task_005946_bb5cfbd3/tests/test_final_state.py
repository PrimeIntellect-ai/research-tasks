# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/locales.db"

def test_database_exists():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."

def test_table_schema():
    assert os.path.isfile(DB_PATH), "Database file missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='translations';")
    table = cursor.fetchone()
    assert table is not None, "Table 'translations' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(translations);")
    columns = cursor.fetchall()
    col_names = [col[1] for col in columns]
    expected_cols = ["key", "lang", "translation"]

    for col in expected_cols:
        assert col in col_names, f"Column '{col}' is missing from the 'translations' table."

    conn.close()

def test_database_content():
    assert os.path.isfile(DB_PATH), "Database file missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT key, lang, translation FROM translations ORDER BY key;")
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        pytest.fail("Failed to query the 'translations' table.")
    finally:
        conn.close()

    expected_rows = [
        ("checkout_item", "es", "Item {{VAR}} añadido a la cesta."),
        ("error_404", "fr", "Page non trouvée pour {{VAR}}"),
        ("greeting_msg", "en", "Hello {{VAR}}, welcome to the system!"),
        ("promo_code", "de", "Der Code {{VAR}} ist ungültig für {{VAR}}.")
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but found {len(rows)}. Ensure the header row was skipped."

    for i, (expected, actual) in enumerate(zip(expected_rows, rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

def test_header_skipped():
    assert os.path.isfile(DB_PATH), "Database file missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM translations WHERE key = 'key' OR lang = 'lang';")
        rows = cursor.fetchall()
        assert len(rows) == 0, "The CSV header row was imported into the database. It should be skipped."
    finally:
        conn.close()
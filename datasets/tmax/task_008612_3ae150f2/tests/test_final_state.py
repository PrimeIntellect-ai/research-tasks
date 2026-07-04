# test_final_state.py

import os
import sqlite3
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_customers.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_database_exists_and_valid():
    db_path = "/home/user/customers.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    # Try connecting to verify it's a valid SQLite database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()
        assert result[0] == "ok", "Database integrity check failed."
    except sqlite3.Error as e:
        pytest.fail(f"Failed to open or query SQLite database: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def test_database_count():
    db_path = "/home/user/customers.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM customers;")
        count = cursor.fetchone()[0]
        assert count == 7, f"Expected 7 records in the customers table, found {count}."
    except sqlite3.Error as e:
        pytest.fail(f"Failed to query customers table: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

def test_recent_customers_csv():
    csv_path = "/home/user/recent_customers.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    expected_content = (
        "2,Bob Jones,5553334444,2020-01-15\n"
        "3,Renée Dupont,15559990000,2021-05-20\n"
        "5,Dave Brown,5556667777,2020-03-10\n"
        "6,Eve White,5557778888,2022-08-22"
    )

    with open(csv_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {csv_path} does not match the expected result.\nExpected:\n{expected_content}\n\nGot:\n{content}"
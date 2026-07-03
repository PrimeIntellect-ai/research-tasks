# test_final_state.py

import os
import sqlite3
import pytest

SCRIPT_PATH = '/home/user/run_audit.sh'
CSV_PATH = '/home/user/suspicious_accounts.csv'
DB_PATH = '/home/user/audit.db'

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_csv_exists():
    assert os.path.exists(CSV_PATH), f"Output file {CSV_PATH} does not exist."
    assert os.path.isfile(CSV_PATH), f"{CSV_PATH} is not a file."

def test_csv_content():
    expected_content = [
        "4,Delta Co,1200.0",
        "1,Alice Corp,700.0"
    ]

    with open(CSV_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_content, (
        f"CSV content does not match expected.\n"
        f"Expected:\n{expected_content}\n"
        f"Found:\n{lines}"
    )

def test_indexes_created():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if there are user-created indexes on the transactions table
    c.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='index' AND tbl_name='transactions' AND name NOT LIKE 'sqlite_autoindex%'
    """)
    indexes = c.fetchall()
    conn.close()

    assert len(indexes) > 0, "No indexes were created on the 'transactions' table to optimize the query."
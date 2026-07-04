# test_final_state.py

import os
import sqlite3

def test_crash_id_file():
    """Verify that crash_id.txt exists and contains the correct transaction ID."""
    file_path = '/home/user/crash_id.txt'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content == "TXN-0452", f"Expected 'TXN-0452' in {file_path}, but found '{content}'."

def test_total_processed_file():
    """Verify that total_processed.txt exists and contains the correct count."""
    file_path = '/home/user/total_processed.txt'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content == "1000", f"Expected '1000' in {file_path}, but found '{content}'."

def test_database_records():
    """Verify that the database contains exactly 1000 records and data is properly decoded."""
    db_path = '/home/user/transactions.db'
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Check table existence
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
    assert c.fetchone() is not None, "Table 'transactions' does not exist in the database."

    # Check total count
    c.execute("SELECT COUNT(*) FROM transactions")
    count = c.fetchone()[0]
    assert count == 1000, f"Expected 1000 records in the database, but found {count}."

    # Check specific decoded record (the one that was originally unpadded)
    c.execute("SELECT data FROM transactions WHERE id = 'TXN-0452'")
    row = c.fetchone()
    assert row is not None, "Record 'TXN-0452' is missing from the database."
    assert row[0] == "Data for TXN-0452", f"Expected decoded data 'Data for TXN-0452', but got '{row[0]}'."

    conn.close()
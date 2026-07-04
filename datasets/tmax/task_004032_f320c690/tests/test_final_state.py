# test_final_state.py
import os
import sqlite3
import csv
import pytest

DB_PATH = "/home/user/audit.db"
CSV_PATH = "/home/user/deadlock_risks.csv"

def test_database_exists():
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    assert os.path.isfile(DB_PATH), f"Path {DB_PATH} is not a file"

def test_transactions_table_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(transactions);")
    columns = {row[1] for row in cursor.fetchall()}
    conn.close()

    expected_columns = {"tx_id", "account_id", "start_time", "end_time", "operation"}
    missing = expected_columns - columns
    assert not missing, f"The 'transactions' table is missing columns: {missing}"

def test_database_index_exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA index_list(transactions);")
    indexes = cursor.fetchall()

    found_valid_index = False
    for idx in indexes:
        index_name = idx[1]
        cursor.execute(f"PRAGMA index_info({index_name});")
        idx_cols = [row[2] for row in cursor.fetchall()]

        # Check if index contains account_id and start_time (order matters for the query optimization, 
        # but we can accept if both are in the index, typically account_id first)
        if "account_id" in idx_cols and "start_time" in idx_cols:
            found_valid_index = True
            break

    conn.close()
    assert found_valid_index, "No index found on 'transactions' table covering 'account_id' and 'start_time'"

def test_csv_file_exists():
    assert os.path.exists(CSV_PATH), f"CSV file missing at {CSV_PATH}"
    assert os.path.isfile(CSV_PATH), f"Path {CSV_PATH} is not a file"

def test_csv_contents():
    expected_rows = [
        ["account_id", "current_tx", "next_tx"],
        ["A900", "tx20", "tx21"],
        ["A800", "tx18", "tx19"],
        ["A700", "tx16", "tx17"],
        ["A600", "tx13", "tx14"],
        ["A500", "tx11", "tx12"],
        ["A400", "tx08", "tx09"],
        ["A400", "tx09", "tx10"],
        ["A200", "tx04", "tx05"],
        ["A200", "tx05", "tx06"],
        ["A100", "tx01", "tx02"]
    ]

    actual_rows = []
    with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append(row)

    assert actual_rows == expected_rows, (
        f"CSV contents do not match expected results.\n"
        f"Expected: {expected_rows}\n"
        f"Actual: {actual_rows}"
    )
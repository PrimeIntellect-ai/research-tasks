# test_final_state.py

import os
import sqlite3
import csv
import pytest

RESULTS_CSV_PATH = '/home/user/results.csv'
PLAN_TXT_PATH = '/home/user/plan.txt'
DB_PATH = '/home/user/compliance.db'

def test_results_csv_content():
    """Verify that results.csv exists and contains the correct data."""
    assert os.path.exists(RESULTS_CSV_PATH), f"{RESULTS_CSV_PATH} does not exist."
    assert os.path.isfile(RESULTS_CSV_PATH), f"{RESULTS_CSV_PATH} is not a file."

    expected_rows = [
        ['log_id', 'emp_name', 'asset_name', 'access_time'],
        ['2', 'Bob', 'Payroll DB', '2023-10-02 11:30:00'],
        ['4', 'Alice', 'Employee Records', '2023-10-15 14:20:00']
    ]

    with open(RESULTS_CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, f"CSV content does not match the expected output. Got: {actual_rows}"

def test_plan_txt_exists_and_valid():
    """Verify that plan.txt exists and looks like EXPLAIN QUERY PLAN output."""
    assert os.path.exists(PLAN_TXT_PATH), f"{PLAN_TXT_PATH} does not exist."
    assert os.path.isfile(PLAN_TXT_PATH), f"{PLAN_TXT_PATH} is not a file."

    with open(PLAN_TXT_PATH, 'r') as f:
        content = f.read().upper()

    # EXPLAIN QUERY PLAN typically outputs lines containing 'SEARCH', 'SCAN', 'USE TEMP B-TREE', etc.
    assert 'SCAN' in content or 'SEARCH' in content, f"{PLAN_TXT_PATH} does not appear to contain valid EXPLAIN QUERY PLAN output."

def test_indexes_created():
    """Verify that the script created indexes to optimize the query."""
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No custom indexes were found in the database. The script was supposed to create indexes to optimize the query."
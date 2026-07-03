# test_final_state.py

import os
import sqlite3
import csv
import pytest

DB_PATH = '/home/user/company.db'
PLAN_BEFORE_PATH = '/home/user/plan_before.txt'
PLAN_AFTER_PATH = '/home/user/plan_after.txt'
REPORTS_CSV_PATH = '/home/user/reports.csv'

def test_plan_before():
    """Verify that plan_before.txt exists and indicates a SCAN."""
    assert os.path.exists(PLAN_BEFORE_PATH), f"{PLAN_BEFORE_PATH} does not exist."
    with open(PLAN_BEFORE_PATH, 'r', encoding='utf-8') as f:
        content = f.read().upper()
    assert "SCAN" in content, f"Expected to find 'SCAN' in {PLAN_BEFORE_PATH}, but it was not found."

def test_idx_manager_exists():
    """Verify that the idx_manager index was created."""
    assert os.path.exists(DB_PATH), f"{DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_manager';")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "Index 'idx_manager' does not exist in the database."

def test_plan_after():
    """Verify that plan_after.txt exists and indicates a SEARCH using idx_manager."""
    assert os.path.exists(PLAN_AFTER_PATH), f"{PLAN_AFTER_PATH} does not exist."
    with open(PLAN_AFTER_PATH, 'r', encoding='utf-8') as f:
        content = f.read().upper()

    assert "SEARCH" in content or "INDEX" in content, f"Expected to find 'SEARCH' or 'INDEX' in {PLAN_AFTER_PATH}."
    assert "IDX_MANAGER" in content, f"Expected to find reference to 'idx_manager' in {PLAN_AFTER_PATH}."

def test_reports_csv():
    """Verify that reports.csv exists, has the correct header, and contains the correct data."""
    assert os.path.exists(REPORTS_CSV_PATH), f"{REPORTS_CSV_PATH} does not exist."

    # Compute the expected result from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        WITH RECURSIVE org_chart AS (
            SELECT id, name, manager_id FROM employees WHERE id = 42
            UNION ALL
            SELECT e.id, e.name, e.manager_id 
            FROM employees e
            JOIN org_chart o ON e.manager_id = o.id
        )
        SELECT id, name, manager_id FROM org_chart ORDER BY id ASC;
    ''')
    expected_rows = cursor.fetchall()
    conn.close()

    # Read the CSV file
    with open(REPORTS_CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"{REPORTS_CSV_PATH} is empty.")

        assert header == ['id', 'name', 'manager_id'], f"Incorrect CSV header. Expected ['id', 'name', 'manager_id'], got {header}"

        actual_rows = []
        for row in reader:
            if len(row) != 3:
                pytest.fail(f"Row {row} does not have 3 columns.")
            # Convert types to match expected_rows
            emp_id = int(row[0])
            name = row[1]
            manager_id = int(row[2]) if row[2] else None
            actual_rows.append((emp_id, name, manager_id))

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, but found {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."
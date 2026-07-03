# test_final_state.py
import os
import csv
import sqlite3
import pytest

DB_PATH = "/home/user/company.db"
SCRIPT_PATH = "/home/user/process_salaries.py"
CSV_PATH = "/home/user/department_summary.csv"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Python script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_csv_exists():
    assert os.path.exists(CSV_PATH), f"CSV file missing at {CSV_PATH}"
    assert os.path.isfile(CSV_PATH), f"{CSV_PATH} is not a file"

def test_csv_content():
    with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 1, "CSV file is empty"

    header = rows[0]
    assert header == ['department_name', 'total_salary'], f"Incorrect CSV header: {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected 3 data rows in CSV, found {len(data_rows)}"

    expected_data = {
        'Engineering': 230000,
        'Sales': 175000,
        'Marketing': 75000
    }

    actual_data = {}
    for row in data_rows:
        assert len(row) == 2, f"Expected 2 columns in row, found {len(row)}: {row}"
        dept, salary_str = row
        try:
            salary = int(salary_str)
        except ValueError:
            pytest.fail(f"Salary for {dept} is not a valid integer: {salary_str}")
        actual_data[dept] = salary

    assert actual_data == expected_data, f"CSV data mismatch. Expected {expected_data}, got {actual_data}"

def test_db_integrity():
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    result = cursor.fetchone()
    conn.close()
    assert result and result[0] == "ok", "Database integrity check failed"
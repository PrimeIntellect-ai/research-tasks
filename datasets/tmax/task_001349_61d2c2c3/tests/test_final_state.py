# test_final_state.py
import os
import sqlite3
import pytest

CPP_PATH = "/home/user/auditor.cpp"
BIN_PATH = "/home/user/auditor"
CSV_PATH = "/home/user/audit_report.csv"
DB_PATH = "/home/user/audit.db"

EXPECTED_CSV_CONTENT = """tx_id,emp_name,amount,top_manager_name
104,Eve,1500.0,Alice
108,Grace,3000.0,Alice
"""

def test_source_code_exists():
    """Test that the C++ source file exists."""
    assert os.path.exists(CPP_PATH), f"Source file {CPP_PATH} does not exist."
    assert os.path.isfile(CPP_PATH), f"Path {CPP_PATH} is not a file."

def test_binary_exists_and_executable():
    """Test that the compiled binary exists and is executable."""
    assert os.path.exists(BIN_PATH), f"Compiled binary {BIN_PATH} does not exist."
    assert os.path.isfile(BIN_PATH), f"Path {BIN_PATH} is not a file."
    assert os.access(BIN_PATH, os.X_OK), f"Binary {BIN_PATH} is not executable."

def test_csv_report_content():
    """Test that the CSV report exists and contains the correct data."""
    assert os.path.exists(CSV_PATH), f"CSV report {CSV_PATH} does not exist."
    assert os.path.isfile(CSV_PATH), f"Path {CSV_PATH} is not a file."

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize line endings
    content = content.replace("\r\n", "\n").strip()
    expected = EXPECTED_CSV_CONTENT.strip()

    assert content == expected, f"CSV content does not match expected output.\nExpected:\n{expected}\nGot:\n{content}"

def test_database_unmodified():
    """Test that the database was not modified."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check employees table
        cursor.execute("SELECT count(*) FROM employees")
        emp_count = cursor.fetchone()[0]
        assert emp_count == 7, f"Expected 7 rows in employees table, found {emp_count}. Database was modified."

        # Check transactions table
        cursor.execute("SELECT count(*) FROM transactions")
        tx_count = cursor.fetchone()[0]
        assert tx_count == 8, f"Expected 8 rows in transactions table, found {tx_count}. Database was modified."

    except sqlite3.Error as e:
        pytest.fail(f"SQLite error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
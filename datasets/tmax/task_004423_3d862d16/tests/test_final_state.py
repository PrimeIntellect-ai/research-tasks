# test_final_state.py
import os
import sqlite3
import csv
import stat
import pytest

DB_PATH = '/home/user/corp_data.db'
CPP_SOURCE_PATH = '/home/user/audit_tool.cpp'
BINARY_PATH = '/home/user/audit_tool'
REPORT_PATH = '/home/user/audit_report.csv'

def test_source_and_binary_exist():
    assert os.path.exists(CPP_SOURCE_PATH), f"C++ source code missing at {CPP_SOURCE_PATH}"
    assert os.path.exists(BINARY_PATH), f"Compiled binary missing at {BINARY_PATH}"

    # Check if binary is executable
    st = os.stat(BINARY_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {BINARY_PATH} is not executable"

def test_database_indexes_created():
    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = {row[0] for row in c.fetchall()}

    assert 'idx_comm_filter' in indexes, "Index 'idx_comm_filter' was not created on the database"
    assert 'idx_comm_edges' in indexes, "Index 'idx_comm_edges' was not created on the database"
    conn.close()

def test_audit_report_content():
    assert os.path.exists(REPORT_PATH), f"Audit report missing at {REPORT_PATH}"

    with open(REPORT_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Audit report is empty"

    # Check header
    header = rows[0]
    expected_header = ['EmployeeID', 'Name', 'Department', 'InDegree', 'OutDegree', 'BrokerScore']
    assert header == expected_header, f"Expected header {expected_header}, but got {header}"

    # Check data rows
    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected exactly 3 data rows based on limit=3, but got {len(data_rows)}"

    expected_data = [
        ['2', 'Bob', 'Engineering', '3', '3', '9'],
        ['3', 'Charlie', 'Engineering', '1', '2', '2'],
        ['1', 'Alice', 'HR', '0', '1', '0']
    ]

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}"
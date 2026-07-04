# test_final_state.py

import os
import sqlite3
import csv
import pytest

DB_PATH = "/home/user/audit.db"
CSV_PATH = "/home/user/co_access_graph.csv"
C_SRC_PATH = "/home/user/audit_graph.c"

def test_c_source_exists():
    """Test that the C source code file was created."""
    assert os.path.exists(C_SRC_PATH), f"C source file missing at {C_SRC_PATH}"
    assert os.path.isfile(C_SRC_PATH), f"Path {C_SRC_PATH} is not a file"

def test_output_csv_exists():
    """Test that the output CSV file was generated."""
    assert os.path.exists(CSV_PATH), f"Output CSV missing at {CSV_PATH}"
    assert os.path.isfile(CSV_PATH), f"Path {CSV_PATH} is not a file"

def test_co_access_graph_contents():
    """Test that the CSV contents exactly match the expected co-access graph."""
    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"
    assert os.path.exists(CSV_PATH), f"Output CSV missing at {CSV_PATH}"

    # Compute expected data directly from the SQLite database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    WITH aggregated_access AS (
        SELECT emp_id, resource_id, SUM(access_count) as total_access
        FROM access_logs
        GROUP BY emp_id, resource_id
    )
    SELECT 
        m.emp_id AS Manager_ID,
        s.emp_id AS Subordinate_ID,
        a1.resource_id AS Resource_ID,
        a1.total_access AS Manager_Total_Accesses,
        a2.total_access AS Subordinate_Total_Accesses
    FROM employees s
    JOIN employees m ON s.manager_id = m.emp_id
    JOIN aggregated_access a1 ON m.emp_id = a1.emp_id
    JOIN aggregated_access a2 ON s.emp_id = a2.emp_id AND a1.resource_id = a2.resource_id
    ORDER BY Manager_ID ASC, Subordinate_ID ASC, Resource_ID ASC;
    """
    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    # Read actual data from the generated CSV
    actual_rows = []
    with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            assert len(row) == 5, f"Expected 5 columns in CSV, got {len(row)} in row: {row}"
            try:
                manager_id = int(row[0])
                sub_id = int(row[1])
                resource_id = row[2]
                manager_acc = int(row[3])
                sub_acc = int(row[4])
                actual_rows.append((manager_id, sub_id, resource_id, manager_acc, sub_acc))
            except ValueError as e:
                pytest.fail(f"Failed to parse CSV row as expected types (integers for IDs and counts): {row}. Error: {e}")

    # Compare lengths first for a clearer error message
    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in the CSV, but found {len(actual_rows)}."

    # Compare the actual rows to the expected rows
    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, \
            f"Row {i+1} mismatch. Expected {expected}, got {actual}. Ensure correct sorting and aggregation."
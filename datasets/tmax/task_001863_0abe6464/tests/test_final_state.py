# test_final_state.py

import os
import sqlite3
import csv
import pytest

DB_PATH = "/home/user/audit.db"
C_SOURCE_PATH = "/home/user/audit_processor.c"
EXEC_PATH = "/home/user/audit_processor"
CSV_PATH = "/home/user/audit_results.csv"

def get_expected_results(db_path, manager_id, threshold):
    """Compute the expected results directly from the database using the specified logic."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    WITH RECURSIVE subordinates AS (
        SELECT emp_id, name, manager_id
        FROM employees
        WHERE emp_id = ?

        UNION ALL

        SELECT e.emp_id, e.name, e.manager_id
        FROM employees e
        INNER JOIN subordinates s ON e.manager_id = s.emp_id
    ),
    aggregated AS (
        SELECT s.emp_id, s.name, a.resource_id, SUM(a.bytes_transferred) as total_bytes
        FROM subordinates s
        JOIN access_logs a ON s.emp_id = a.emp_id
        GROUP BY s.emp_id, s.name, a.resource_id
    ),
    ranked AS (
        SELECT emp_id, name, resource_id, total_bytes,
               ROW_NUMBER() OVER (PARTITION BY resource_id ORDER BY total_bytes DESC, emp_id ASC) as rank
        FROM aggregated
    )
    SELECT emp_id, name, resource_id, total_bytes, rank
    FROM ranked
    WHERE total_bytes > ?
    ORDER BY resource_id ASC, rank ASC;
    """

    cursor.execute(query, (manager_id, threshold))
    rows = cursor.fetchall()
    conn.close()

    return rows

def test_c_source_exists():
    """Verify that the C source code was created."""
    assert os.path.exists(C_SOURCE_PATH), f"C source file {C_SOURCE_PATH} is missing."
    assert os.path.isfile(C_SOURCE_PATH), f"{C_SOURCE_PATH} is not a regular file."

def test_executable_exists():
    """Verify that the C program was compiled into an executable."""
    assert os.path.exists(EXEC_PATH), f"Compiled executable {EXEC_PATH} is missing. Did you compile the C program?"
    assert os.path.isfile(EXEC_PATH), f"{EXEC_PATH} is not a regular file."
    assert os.access(EXEC_PATH, os.X_OK), f"{EXEC_PATH} is not executable."

def test_csv_results():
    """Verify that the output CSV exists, has the correct header, and contains exactly the expected data."""
    assert os.path.exists(CSV_PATH), f"Results CSV file {CSV_PATH} is missing. Did the program run successfully?"

    # Compute the expected results based on the current state of the database
    expected_rows = get_expected_results(DB_PATH, 1, 500)

    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        expected_header = ["emp_id", "name", "resource_id", "total_bytes", "rank"]
        assert header == expected_header, f"CSV header is incorrect.\nExpected: {expected_header}\nActual: {header}"

        actual_rows = []
        for i, row in enumerate(reader, start=2):
            if not row:
                continue
            try:
                actual_rows.append((int(row[0]), row[1], int(row[2]), int(row[3]), int(row[4])))
            except ValueError as e:
                pytest.fail(f"Data format error in CSV at line {i}: {row}. Error: {e}")

    assert actual_rows == expected_rows, (
        f"CSV contents do not match the expected SQL results.\n"
        f"Expected: {expected_rows}\n"
        f"Actual:   {actual_rows}"
    )
# test_final_state.py

import os
import sqlite3
import pytest
import csv

def test_analyzer_cpp_exists_and_uses_sqlite():
    """Verify that the C++ source file exists and uses sqlite3 API."""
    cpp_path = "/home/user/analyzer.cpp"
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."

    with open(cpp_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "sqlite3_" in content, "The C++ program does not appear to use the sqlite3 API."
    assert "<sqlite3.h>" in content, "The C++ program does not include <sqlite3.h>."

def test_analyzer_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    exe_path = "/home/user/analyzer"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did it compile successfully?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_query_plan_output():
    """Verify that query_plan.txt exists and contains EXPLAIN QUERY PLAN output."""
    plan_path = "/home/user/query_plan.txt"
    assert os.path.isfile(plan_path), f"Query plan output file {plan_path} does not exist."

    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read().upper()

    # EXPLAIN QUERY PLAN output typically contains keywords like SCAN, SEARCH, USING INDEX
    assert "SCAN" in content or "SEARCH" in content or "USING" in content, \
        f"File {plan_path} does not seem to contain valid EXPLAIN QUERY PLAN output."

def test_database_indexes_updated():
    """Verify that the old index was dropped and a new index exists."""
    db_path = "/home/user/ecommerce.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='transactions'")
    indexes = {row[0] for row in cursor.fetchall()}

    assert 'idx_bad' not in indexes, "The corrupted index 'idx_bad' was not dropped."
    assert len(indexes) > 0, "No new indexes were created on the transactions table."

    conn.close()

def test_report_csv_correctness():
    """Verify that report.csv exists and contains the correct aggregated data."""
    csv_path = "/home/user/report.csv"
    db_path = "/home/user/ecommerce.db"

    assert os.path.isfile(csv_path), f"Report file {csv_path} does not exist."
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    # Calculate expected results dynamically
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT u.name, SUM(t.amount) as total_volume, ROUND(AVG(t.amount), 2) as avg_amount
    FROM users u
    JOIN transactions t ON u.id = t.user_id
    JOIN products p ON t.product_id = p.id
    WHERE p.category = 'Electronics'
      AND t.tx_date BETWEEN '2023-10-01' AND '2023-12-31'
    GROUP BY u.id
    ORDER BY total_volume DESC, u.name ASC
    LIMIT 5;
    """

    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    # Read the generated CSV
    actual_rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                actual_rows.append(row)

    assert len(actual_rows) > 0, f"File {csv_path} is empty."

    # Check header if present, otherwise just check data
    start_idx = 0
    if actual_rows[0][0] == "user_name":
        start_idx = 1

    data_rows = actual_rows[start_idx:]
    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but found {len(data_rows)}."

    for i in range(len(expected_rows)):
        expected_name = expected_rows[i][0]
        expected_total = f"{expected_rows[i][1]:.2f}"
        expected_avg = f"{expected_rows[i][2]:.2f}"

        actual_name = data_rows[i][0]
        actual_total = f"{float(data_rows[i][1]):.2f}"
        actual_avg = f"{float(data_rows[i][2]):.2f}"

        assert actual_name == expected_name, f"Row {i+1}: Expected user_name '{expected_name}', got '{actual_name}'."
        assert actual_total == expected_total, f"Row {i+1}: Expected total_volume '{expected_total}', got '{actual_total}'."
        assert actual_avg == expected_avg, f"Row {i+1}: Expected avg_amount '{expected_avg}', got '{actual_avg}'."
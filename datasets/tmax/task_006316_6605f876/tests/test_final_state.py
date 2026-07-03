# test_final_state.py

import os
import sqlite3
import csv
import pytest

DB_PATH = "/home/user/data/architecture.db"
CSV_PATH = "/home/user/extracted_paths.csv"
LOG_PATH = "/home/user/query_plan.log"

def test_idx_bad_edges_dropped():
    assert os.path.exists(DB_PATH), "Database file is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_bad_edges'")
    index = cursor.fetchone()
    conn.close()
    assert index is None, "The index 'idx_bad_edges' was not dropped."

def test_new_indexes_created():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name != 'sqlite_autoindex_nodes_1'")
    indexes = cursor.fetchall()
    conn.close()
    assert len(indexes) > 0, "No new indexes were created to optimize the query."

def test_extracted_paths_csv_exists_and_correct():
    assert os.path.exists(CSV_PATH), f"CSV file missing at {CSV_PATH}"

    # Recompute the expected results
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT e1.source, e2.source, e3.source, e3.target
        FROM edges e1
        JOIN edges e2 ON e1.target = e2.source
        JOIN edges e3 ON e2.target = e3.source
        JOIN nodes n1 ON e1.source = n1.id
        JOIN nodes n4 ON e3.target = n4.id
        WHERE e1.relation = 'calls' 
          AND e2.relation = 'calls' 
          AND e3.relation = 'calls'
          AND n1.type = 'Gateway' 
          AND n4.type = 'Database'
        ORDER BY e1.source, e2.source, e3.source, e3.target
    """
    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_header = ["gateway_id", "service1_id", "service2_id", "database_id"]

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("CSV file is empty.")

        assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}"

        actual_rows = []
        for row in reader:
            if row:
                actual_rows.append(tuple(row))

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}"

def test_query_plan_log():
    assert os.path.exists(LOG_PATH), f"Query plan log missing at {LOG_PATH}"
    with open(LOG_PATH, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert len(content) > 0, "Query plan log is empty."
    # A basic check to see if it looks like an EXPLAIN QUERY PLAN output
    # SQLite EXPLAIN QUERY PLAN usually contains words like 'SCAN', 'SEARCH', 'COVERING INDEX', etc.
    assert any(keyword in content.upper() for keyword in ["SCAN", "SEARCH", "INDEX", "CORRELATED"]), \
        "The file does not appear to contain a valid EXPLAIN QUERY PLAN output."
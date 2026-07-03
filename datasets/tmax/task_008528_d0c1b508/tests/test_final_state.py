# test_final_state.py

import os
import sqlite3
import csv
import pytest

DB_PATH = "/home/user/logistics.db"
CSV_PATH = "/home/user/optimal_route.csv"

def test_database_and_tables_exist():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='routes'")
    assert cursor.fetchone() is not None, "Table 'routes' does not exist in the database."

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='path_sequence'")
    assert cursor.fetchone() is not None, "Table 'path_sequence' does not exist in the database."

    conn.close()

def test_routes_index_exists():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check for index on routes table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='routes'")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No index found on 'routes' table."

    # Verify the index is a composite index on source_city and target_city
    index_found = False
    for idx in indexes:
        index_name = idx[0]
        # Ignore auto-created indexes for sqlite (like sqlite_autoindex)
        if index_name.startswith("sqlite_"):
            continue

        cursor.execute(f"PRAGMA index_info('{index_name}')")
        columns = [row[2] for row in cursor.fetchall()]
        if "source_city" in columns and "target_city" in columns:
            index_found = True
            break

    assert index_found, "Composite index on 'source_city' and 'target_city' is missing."
    conn.close()

def test_optimal_route_csv():
    assert os.path.exists(CSV_PATH), f"Output CSV file {CSV_PATH} is missing."

    expected_data = [
        ["1", "Alpha", "0.0", "0.0"],
        ["2", "Gamma", "10.0", "10.0"],
        ["3", "Delta", "5.0", "15.0"],
        ["4", "Epsilon", "11.0", "26.0"],
        ["5", "Zeta", "8.0", "34.0"]
    ]

    with open(CSV_PATH, "r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["step_order", "city_name", "hop_cost", "cumulative_cost"], "CSV header is incorrect."

        rows = list(reader)
        assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows, got {len(rows)}."

        for i, (row, expected_row) in enumerate(zip(rows, expected_data)):
            # Convert floats to check values accurately, ignoring trailing zeros
            assert row[0] == expected_row[0], f"Row {i+1} step_order mismatch: {row[0]} != {expected_row[0]}"
            assert row[1] == expected_row[1], f"Row {i+1} city_name mismatch: {row[1]} != {expected_row[1]}"
            assert float(row[2]) == float(expected_row[2]), f"Row {i+1} hop_cost mismatch: {row[2]} != {expected_row[2]}"
            assert float(row[3]) == float(expected_row[3]), f"Row {i+1} cumulative_cost mismatch: {row[3]} != {expected_row[3]}"
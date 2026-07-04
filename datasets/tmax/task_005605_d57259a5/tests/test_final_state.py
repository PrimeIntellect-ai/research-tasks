# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/ecommerce.db"
CPP_PATH = "/home/user/process.cpp"
EXE_PATH = "/home/user/process"
QUERY_PLAN_PATH = "/home/user/query_plan.txt"
CSV_PATH = "/home/user/top_clients.csv"

def test_cpp_and_executable_exist():
    """Test if the C++ source and compiled executable exist."""
    assert os.path.isfile(CPP_PATH), f"C++ source file {CPP_PATH} does not exist."
    assert os.path.isfile(EXE_PATH), f"Executable file {EXE_PATH} does not exist."
    assert os.access(EXE_PATH, os.X_OK), f"File {EXE_PATH} is not executable."

def test_indexes_created():
    """Test if new indexes were created in the database to optimize the query."""
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No custom indexes were created in the database."

def test_query_plan_output():
    """Test if the query plan was written to query_plan.txt."""
    assert os.path.isfile(QUERY_PLAN_PATH), f"Query plan file {QUERY_PLAN_PATH} does not exist."

    with open(QUERY_PLAN_PATH, "r") as f:
        content = f.read().upper()

    assert "SCAN" in content or "SEARCH" in content, (
        f"File {QUERY_PLAN_PATH} does not appear to contain valid EXPLAIN QUERY PLAN output. "
        "Expected to find 'SCAN' or 'SEARCH' operations."
    )

def test_csv_output():
    """Test if the CSV output matches the expected results."""
    assert os.path.isfile(CSV_PATH), f"CSV output file {CSV_PATH} does not exist."

    expected_results = [
        (1, 112.50),
        (3, 105.00),
        (5, 105.00),
        (4, 60.00),
        (2, 52.50)
    ]

    actual_results = []
    with open(CSV_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            assert len(parts) == 2, f"Invalid CSV format in line: '{line}'. Expected 'client_id,total_spend'."

            client_id_str, total_spend_str = parts

            # Check exactly 2 decimal places format
            assert "." in total_spend_str and len(total_spend_str.split(".")[1]) == 2, (
                f"Total spend '{total_spend_str}' is not formatted to exactly 2 decimal places."
            )

            actual_results.append((int(client_id_str), float(total_spend_str)))

    assert len(actual_results) == 5, f"Expected 5 top clients, but found {len(actual_results)}."

    # Sort both lists by total_spend (descending) and then client_id (ascending) to handle ties gracefully
    expected_sorted = sorted(expected_results, key=lambda x: (-x[1], x[0]))
    actual_sorted = sorted(actual_results, key=lambda x: (-x[1], x[0]))

    assert actual_sorted == expected_sorted, (
        f"CSV results do not match expected values.\nExpected (sorted): {expected_sorted}\nActual (sorted): {actual_sorted}"
    )
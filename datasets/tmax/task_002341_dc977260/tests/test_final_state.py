# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/syslogs.db"
SCRIPT_PATH = "/home/user/find_deadlocks.sh"
CSV_PATH = "/home/user/deadlocks.csv"

def get_expected_deadlocks(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT 
        a1.transaction_id AS txn_1,
        a2.transaction_id AS txn_2,
        a1.resource_id AS resource_1,
        a2.resource_id AS resource_2
    FROM lock_events a1
    JOIN lock_events a2 
        ON a1.transaction_id < a2.transaction_id
    JOIN lock_events w1 
        ON w1.transaction_id = a1.transaction_id 
        AND w1.resource_id = a2.resource_id 
        AND w1.event_type = 'WAIT' 
        AND w1.event_timestamp > a1.event_timestamp
    JOIN lock_events w2 
        ON w2.transaction_id = a2.transaction_id 
        AND w2.resource_id = a1.resource_id 
        AND w2.event_type = 'WAIT' 
        AND w2.event_timestamp > a2.event_timestamp
    WHERE a1.event_type = 'ACQUIRE' 
      AND a2.event_type = 'ACQUIRE'
    ORDER BY txn_1, txn_2;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return [",".join(row) for row in results]

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_csv_exists():
    assert os.path.isfile(CSV_PATH), f"Output CSV missing at {CSV_PATH}"

def test_csv_contents():
    expected_lines = get_expected_deadlocks(DB_PATH)

    with open(CSV_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"CSV contents do not match expected deadlocks.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )
# test_final_state.py

import os
import sqlite3
import subprocess
import csv
import pytest

SCRIPT_PATH = "/home/user/audit.sh"
DB_PATH = "/home/user/infrastructure.db"
CSV_PATH = "/home/user/suspicious_access.csv"

def get_expected_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = """
    SELECT 
        u.username,
        a.hostname AS accessed_hostname,
        e.event_time,
        ROW_NUMBER() OVER (PARTITION BY u.uid, a.asset_id ORDER BY e.event_time) as access_rank
    FROM access_events e
    JOIN users u ON e.uid = u.uid
    JOIN assets a ON e.asset_id = a.asset_id
    WHERE a.asset_id IN (
        SELECT c1.from_asset
        FROM connections c1
        JOIN connections c2 ON c1.to_asset = c2.from_asset
        JOIN assets a_rest ON c2.to_asset = a_rest.asset_id
        WHERE a_rest.classification = 'Restricted'
    )
    ORDER BY u.username ASC, e.event_time ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # Convert all to strings to match CSV reading
    return [[str(item) for item in row] for row in rows]

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_output():
    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. Stderr: {result.stderr}"

    # Check if CSV is created
    assert os.path.isfile(CSV_PATH), f"Output file {CSV_PATH} was not created."

    # Read the CSV
    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        actual_rows = list(reader)

    expected_header = ["username", "accessed_hostname", "event_time", "access_rank"]
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}"

    expected_rows = get_expected_data()
    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}"
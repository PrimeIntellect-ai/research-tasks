# test_final_state.py

import os
import stat
import sqlite3
import csv
import pytest

DB_PATH = "/home/user/audit.db"
SCRIPT_PATH = "/home/user/audit_check.sh"
CSV_PATH = "/home/user/suspicious_overlaps.csv"

def get_expected_overlaps(db_path):
    """
    Derives the expected suspicious overlaps directly from the database
    to align with the rubric's intent.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Order by user_id and login_time to check immediately preceding sessions
    cursor.execute("""
        SELECT user_id, ip_address, login_time, logout_time 
        FROM access_logs 
        ORDER BY user_id, login_time
    """)
    rows = cursor.fetchall()
    conn.close()

    overlaps = []
    prev_row = None
    for row in rows:
        if prev_row and prev_row['user_id'] == row['user_id']:
            # Suspicious overlap: login_time strictly before prev logout_time AND different IP
            if row['login_time'] < prev_row['logout_time'] and row['ip_address'] != prev_row['ip_address']:
                overlaps.append({
                    'user_id': str(row['user_id']),
                    'first_ip': prev_row['ip_address'],
                    'second_ip': row['ip_address'],
                    'overlap_start_time': row['login_time']
                })
        prev_row = row
    return overlaps

def test_script_exists_and_executable():
    """Check that the bash script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable by the owner."

def test_index_created():
    """Check that the covering index was created on the database."""
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} is missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_user_login';")
    result = cursor.fetchone()
    conn.close()
    assert result is not None, "The index 'idx_user_login' was not created in the database."

def test_csv_output_matches_expected():
    """Check that the CSV file was generated correctly with the expected headers and data."""
    assert os.path.exists(CSV_PATH), f"Output CSV {CSV_PATH} does not exist. Did the script run successfully?"

    expected_overlaps = get_expected_overlaps(DB_PATH)

    with open(CSV_PATH, "r", newline="") as f:
        reader = csv.DictReader(f)
        actual_overlaps = list(reader)

        # Check headers
        expected_headers = ["user_id", "first_ip", "second_ip", "overlap_start_time"]
        assert reader.fieldnames == expected_headers, \
            f"CSV headers are incorrect. Expected {expected_headers}, got {reader.fieldnames}."

    assert len(actual_overlaps) == len(expected_overlaps), \
        f"Expected {len(expected_overlaps)} rows in CSV, but found {len(actual_overlaps)}."

    for i, (actual, expected) in enumerate(zip(actual_overlaps, expected_overlaps)):
        assert actual['user_id'] == expected['user_id'], f"Row {i+1}: user_id mismatch."
        assert actual['first_ip'] == expected['first_ip'], f"Row {i+1}: first_ip mismatch."
        assert actual['second_ip'] == expected['second_ip'], f"Row {i+1}: second_ip mismatch."
        assert actual['overlap_start_time'] == expected['overlap_start_time'], f"Row {i+1}: overlap_start_time mismatch."
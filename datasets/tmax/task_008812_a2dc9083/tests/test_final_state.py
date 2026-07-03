# test_final_state.py

import os
import csv
import sqlite3
import pytest

LOG_FILE = "/home/user/server_logs.csv"
CSV_OUT = "/home/user/anomalies.csv"
DB_OUT = "/home/user/alerts.db"

def compute_expected_anomalies():
    assert os.path.isfile(LOG_FILE), f"Source file {LOG_FILE} is missing."

    windows = {}
    first_ts = None

    with open(LOG_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            ts = int(row[0])
            ip = row[1]

            if first_ts is None:
                first_ts = ts

            # Calculate window index
            # The windows should start aligned to the nearest 10-second boundary 
            # based on the very first timestamp in the file.
            # Example: first_ts = 1000, ts = 1005 -> window 0 (1000)
            window_idx = (ts - first_ts) // 10
            window_start = first_ts + window_idx * 10

            if window_start not in windows:
                windows[window_start] = {'count': 0, 'ips': set()}

            windows[window_start]['count'] += 1
            windows[window_start]['ips'].add(ip)

    # Sort window starts
    sorted_starts = sorted(windows.keys())

    # We need to compute anomalies
    # Anomaly if count > 3 * avg(prev 5 windows)
    expected_rows = []

    # Create a list of counts for easy access, aligned with sorted_starts
    # Note: there might be empty windows if no logs exist, but the problem says "strictly previous 5 windows".
    # We should reconstruct the full sequence of windows from 0 to max_idx just in case, 
    # but based on the setup, windows are contiguous.
    if not sorted_starts:
        return []

    max_idx = (sorted_starts[-1] - first_ts) // 10
    window_counts = [0] * (max_idx + 1)
    for start in sorted_starts:
        idx = (start - first_ts) // 10
        window_counts[idx] = windows[start]['count']

    for start in sorted_starts:
        idx = (start - first_ts) // 10
        if idx >= 5:
            prev_5_sum = sum(window_counts[idx-5:idx])
            avg_prev_5 = prev_5_sum / 5.0

            if window_counts[idx] > 3 * avg_prev_5:
                # Anomaly!
                unique_ips = sorted(list(windows[start]['ips']))
                for ip in unique_ips:
                    expected_rows.append((start, ip, window_counts[idx]))

    return expected_rows

def test_anomalies_csv():
    expected = compute_expected_anomalies()
    assert os.path.isfile(CSV_OUT), f"Output file {CSV_OUT} is missing."

    actual = []
    with open(CSV_OUT, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            assert len(row) == 3, f"Invalid row length in {CSV_OUT}: {row}"
            actual.append((int(row[0]), row[1], int(row[2])))

    # Sort actual just in case, though it should be sorted
    actual_sorted = sorted(actual, key=lambda x: (x[0], x[1]))
    expected_sorted = sorted(expected, key=lambda x: (x[0], x[1]))

    assert actual_sorted == expected_sorted, f"Data in {CSV_OUT} does not match expected anomalies."

def test_alerts_db():
    expected = compute_expected_anomalies()
    assert os.path.isfile(DB_OUT), f"Database file {DB_OUT} is missing."

    conn = sqlite3.connect(DB_OUT)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='anomalies';")
    assert cursor.fetchone() is not None, "Table 'anomalies' does not exist in the database."

    # Check data
    cursor.execute("SELECT window_start, ip, count FROM anomalies ORDER BY window_start ASC, ip ASC;")
    rows = cursor.fetchall()
    conn.close()

    actual = []
    for row in rows:
        actual.append((int(row[0]), row[1], int(row[2])))

    expected_sorted = sorted(expected, key=lambda x: (x[0], x[1]))
    assert actual == expected_sorted, f"Data in {DB_OUT} does not match expected anomalies."
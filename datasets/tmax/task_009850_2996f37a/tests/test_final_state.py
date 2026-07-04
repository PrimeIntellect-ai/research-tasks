# test_final_state.py

import os
import re
import sqlite3
import pytest

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def process_logs(raw_logs_path):
    log_pattern = re.compile(r'^\[(.*?)\] (.*?) "(.*?) (.*?) (.*?)" (\d+) "(.*?)" "(.*?)"$')
    baseline_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    seen_sessions = set()
    processed_records = []

    with open(raw_logs_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = log_pattern.match(line)
            if not match:
                continue

            timestamp, ip, method, path, protocol, status, ua, session_id = match.groups()

            if session_id in seen_sessions:
                continue
            seen_sessions.add(session_id)

            # Clean path
            cleaned_path = re.sub(r'/+', '/', path)

            # Compute distance
            distance = levenshtein_distance(ua, baseline_ua)

            processed_records.append((
                timestamp,
                ip,
                cleaned_path,
                int(status),
                session_id,
                distance
            ))

    return processed_records

def test_processed_csv_exists_and_correct():
    raw_logs_path = "/home/user/raw_logs.txt"
    csv_path = "/home/user/processed_logs.csv"

    assert os.path.exists(raw_logs_path), f"Raw logs file missing: {raw_logs_path}"
    assert os.path.exists(csv_path), f"Processed CSV file missing: {csv_path}"

    expected_records = process_logs(raw_logs_path)

    with open(csv_path, "r") as f:
        csv_lines = [line.strip() for line in f if line.strip()]

    assert len(csv_lines) == len(expected_records), f"Expected {len(expected_records)} rows in CSV, found {len(csv_lines)}"

    for i, expected in enumerate(expected_records):
        expected_line = f"{expected[0]},{expected[1]},{expected[2]},{expected[3]},{expected[4]},{expected[5]}"
        assert csv_lines[i] == expected_line, f"CSV line {i+1} mismatch. Expected: {expected_line}, Got: {csv_lines[i]}"

def test_sqlite_database_exists_and_correct():
    raw_logs_path = "/home/user/raw_logs.txt"
    db_path = "/home/user/logs.db"

    assert os.path.exists(db_path), f"SQLite database missing: {db_path}"

    expected_records = process_logs(raw_logs_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cleaned_logs'")
    assert cursor.fetchone() is not None, "Table 'cleaned_logs' does not exist in the database."

    # Check row count
    cursor.execute("SELECT COUNT(*) FROM cleaned_logs")
    count = cursor.fetchone()[0]
    assert count == len(expected_records), f"Expected {len(expected_records)} rows in 'cleaned_logs' table, found {count}"

    # Check data
    cursor.execute("SELECT timestamp, ip_address, path, status_code, session_id, ua_distance FROM cleaned_logs ORDER BY session_id")
    db_rows = cursor.fetchall()

    expected_sorted = sorted(expected_records, key=lambda x: x[4])

    for i, (expected, db_row) in enumerate(zip(expected_sorted, db_rows)):
        assert str(db_row[0]) == expected[0], f"Row {i} timestamp mismatch"
        assert str(db_row[1]) == expected[1], f"Row {i} ip_address mismatch"
        assert str(db_row[2]) == expected[2], f"Row {i} path mismatch"
        assert int(db_row[3]) == expected[3], f"Row {i} status_code mismatch"
        assert str(db_row[4]) == expected[4], f"Row {i} session_id mismatch"
        assert int(db_row[5]) == expected[5], f"Row {i} ua_distance mismatch"

    conn.close()
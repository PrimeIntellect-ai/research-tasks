# test_final_state.py

import os
import sqlite3
import csv
import subprocess
import pytest

def test_db_index_dropped():
    db_path = "/app/data/network.db"
    assert os.path.exists(db_path), f"Database missing at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_stale_cache';")
    result = cursor.fetchall()
    conn.close()

    assert len(result) == 0, "Index 'idx_stale_cache' was not dropped from the database."

def test_cumulative_report():
    db_path = "/app/data/network.db"
    assert os.path.exists(db_path), f"Database missing at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender, timestamp, SUM(amount) OVER (PARTITION BY sender ORDER BY timestamp) as cumulative_amount
        FROM transactions
    """)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_rows_sorted = sorted([(str(r[0]), str(r[1]), float(r[2])) for r in expected_rows])

    csv_path = "/home/user/cumulative_report.csv"
    assert os.path.exists(csv_path), f"Cumulative report missing at {csv_path}"

    actual_rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row:
                continue
            try:
                actual_rows.append((str(row[0]), str(row[1]), float(row[2])))
            except ValueError:
                pytest.fail(f"Could not parse row in CSV: {row}")

    actual_rows_sorted = sorted(actual_rows)

    assert len(actual_rows_sorted) == len(expected_rows_sorted), "Number of rows in cumulative report does not match expected."

    for actual, expected in zip(actual_rows_sorted, expected_rows_sorted):
        assert actual[0] == expected[0], f"Sender mismatch: {actual[0]} != {expected[0]}"
        assert actual[1] == expected[1], f"Timestamp mismatch: {actual[1]} != {expected[1]}"
        assert abs(actual[2] - expected[2]) < 1e-5, f"Cumulative amount mismatch for {actual[0]} at {actual[1]}: {actual[2]} != {expected[2]}"

def test_classifier_corpus():
    script_path = "/home/user/classifier.py"
    assert os.path.exists(script_path), f"Classifier script missing at {script_path}"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_failures = []
    evil_failures = []

    clean_count = 0
    evil_count = 0

    if os.path.exists(clean_dir):
        for f in os.listdir(clean_dir):
            if not f.endswith(".csv"): continue
            clean_count += 1
            file_path = os.path.join(clean_dir, f)
            result = subprocess.run(["python3", script_path, file_path], capture_output=True, text=True)
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_failures.append(f)

    if os.path.exists(evil_dir):
        for f in os.listdir(evil_dir):
            if not f.endswith(".csv"): continue
            evil_count += 1
            file_path = os.path.join(evil_dir, f)
            result = subprocess.run(["python3", script_path, file_path], capture_output=True, text=True)
            output = result.stdout.strip()
            if output != "EVIL":
                evil_failures.append(f)

    error_msg = []
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {clean_count} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {evil_count} evil bypassed: {', '.join(evil_failures)}")

    assert not error_msg, " | ".join(error_msg)
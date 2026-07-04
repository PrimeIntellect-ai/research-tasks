# test_final_state.py

import os
import sqlite3
import csv
import pytest
from collections import defaultdict

DB_PATH = "/home/user/compliance.db"
CSV_PATH = "/home/user/filtered_tx.csv"
C_FILE_PATH = "/home/user/graph_audit.c"
VIOLATIONS_PATH = "/home/user/violations.txt"

def compute_expected_anomalous(db_path):
    """
    Computes the expected anomalous transactions based on the rules:
    - amount > avg of preceding 2 txns from same src_account by timestamp.
    - If < 2 preceding, avg over available.
    - If 0 preceding, avg = 0.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT tx_id, src_account, dst_account, amount, timestamp FROM transactions ORDER BY src_account, timestamp")
    rows = cursor.fetchall()
    conn.close()

    history = defaultdict(list)
    anomalous = set()

    for row in rows:
        tx_id, src, dst, amt, ts = row
        hist = history[src]

        if len(hist) == 0:
            avg = 0.0
        elif len(hist) == 1:
            avg = hist[0]
        else:
            avg = (hist[-1] + hist[-2]) / 2.0

        if amt > avg:
            anomalous.add(tx_id)

        history[src].append(amt)

    return anomalous

def test_filtered_tx_csv_exists_and_correct():
    """Verify that filtered_tx.csv exists and contains the correct anomalous transactions."""
    assert os.path.isfile(CSV_PATH), f"CSV file not found at {CSV_PATH}"

    expected_anomalous_tx_ids = compute_expected_anomalous(DB_PATH)
    actual_anomalous_tx_ids = set()

    with open(CSV_PATH, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            try:
                tx_id = int(row[0])
                actual_anomalous_tx_ids.add(tx_id)
            except ValueError:
                pytest.fail(f"Invalid tx_id format in CSV: {row[0]}")

    missing = expected_anomalous_tx_ids - actual_anomalous_tx_ids
    extra = actual_anomalous_tx_ids - expected_anomalous_tx_ids

    assert not missing, f"Missing anomalous transactions in CSV: {missing}"
    assert not extra, f"Extra non-anomalous transactions in CSV: {extra}"

def test_c_program_exists():
    """Verify that the C program was created."""
    assert os.path.isfile(C_FILE_PATH), f"C program not found at {C_FILE_PATH}"

def test_violations_output():
    """Verify that violations.txt exists and contains the correct cycle."""
    assert os.path.isfile(VIOLATIONS_PATH), f"Violations output not found at {VIOLATIONS_PATH}"

    with open(VIOLATIONS_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"Expected exactly 1 violation, found {len(lines)}"
    assert lines[0] == "10,20,30", f"Expected violation '10,20,30', found '{lines[0]}'"
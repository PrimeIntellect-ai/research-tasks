# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

def test_flagged_accounts():
    flagged_file = "/home/user/flagged_accounts.txt"
    assert os.path.isfile(flagged_file), f"File {flagged_file} does not exist."

    with open(flagged_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "http://example.org/account/Acc1",
        "http://example.org/account/Acc10",
        "http://example.org/account/Acc2",
        "http://example.org/account/Acc3",
        "http://example.org/account/Acc8",
        "http://example.org/account/Acc9"
    ]

    assert lines == expected, f"Contents of {flagged_file} do not match the expected list of URIs or are not sorted correctly."

def test_deadlock_resolution():
    db_path = "/home/user/audit.db"
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    # Reset the database to ensure a clean test
    conn = sqlite3.connect(db_path)
    conn.execute("UPDATE accounts SET status='pending'")
    conn.commit()
    conn.close()

    worker1 = "/home/user/worker1.py"
    worker2 = "/home/user/worker2.py"

    assert os.path.isfile(worker1), f"{worker1} is missing."
    assert os.path.isfile(worker2), f"{worker2} is missing."

    # Run both scripts concurrently
    p1 = subprocess.Popen(["python3", worker1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(["python3", worker2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    p1.wait()
    p2.wait()

    # Check if both accounts were updated to 'auditing'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, status FROM accounts ORDER BY id")
    rows = cursor.fetchall()
    conn.close()

    expected_rows = [(1, 'auditing'), (2, 'auditing')]
    assert rows == expected_rows, "Deadlock occurred or scripts failed to update both accounts to 'auditing' when run concurrently."

def test_worker2_modified():
    worker2 = "/home/user/worker2.py"
    with open(worker2, "r") as f:
        content = f.read().upper()

    assert "BEGIN IMMEDIATE" in content or "BEGIN EXCLUSIVE" in content, (
        "worker2.py does not appear to use BEGIN IMMEDIATE or BEGIN EXCLUSIVE to prevent deadlocks."
    )
# test_final_state.py

import os
import sqlite3

def test_solution_file_exists():
    assert os.path.isfile("/home/user/solution.txt"), "/home/user/solution.txt is missing. You need to create it with the required answers."

def test_solution_contents():
    secret_path = "/home/user/.secret_bad_commit"
    assert os.path.isfile(secret_path), f"Truth file {secret_path} is missing, cannot verify."

    with open(secret_path, "r") as f:
        expected_commit = f.read().strip()

    with open("/home/user/solution.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 non-empty lines in /home/user/solution.txt, got {len(lines)}."

    actual_commit = lines[0]
    assert actual_commit == expected_commit, (
        f"Line 1 (commit hash) is incorrect. The wrong commit was identified as the first bad commit."
    )

    db_path = "/home/user/tx_analyzer/transactions.db"
    assert os.path.isfile(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT type, amount FROM tx WHERE user_id = 'U15'")
    rows = c.fetchall()
    conn.close()

    expected_balance = 0.0
    for tx_type, amount in rows:
        if tx_type == 'refund':
            expected_balance -= amount
        else:
            expected_balance += amount

    try:
        actual_balance = float(lines[1])
    except ValueError:
        actual_balance = None

    assert actual_balance == expected_balance, (
        f"Line 2 (balance) is incorrect. Expected {expected_balance}, got {lines[1]}."
    )
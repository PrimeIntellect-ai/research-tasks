# test_final_state.py
import os
import sqlite3
import statistics

def test_flagged_accounts_output():
    output_path = "/home/user/flagged_accounts.txt"
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    db_path = "/home/user/transactions.db"
    assert os.path.isfile(db_path), f"Database file missing: {db_path}"

    # Compute expected output directly from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM accounts WHERE status IN ('active', 'suspended')")
    valid_accounts = [row[0] for row in cursor.fetchall()]

    expected_lines = []
    for acc_id in sorted(valid_accounts):
        cursor.execute("SELECT amount FROM transactions WHERE account_id = ?", (acc_id,))
        txs = [row[0] for row in cursor.fetchall()]
        if len(txs) > 1:
            # Using Python's built-in robust statistics library
            sd = statistics.stdev(txs)
            expected_lines.append(f"{acc_id},{sd:.4f}")

    conn.close()

    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Output file contents do not match the expected values.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )
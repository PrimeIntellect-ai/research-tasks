# test_final_state.py
import os
import sqlite3
import pytest

def test_flagged_entities_csv():
    csv_path = '/home/user/flagged_entities.csv'
    db_path = '/home/user/financial_graph.db'

    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    # Compute the expected output from the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    query = """
        SELECT DISTINCT t1.sender_id
        FROM transactions t1
        JOIN transactions t2 ON t1.receiver_id = t2.sender_id
        JOIN transactions t3 ON t2.receiver_id = t3.sender_id
        WHERE t3.receiver_id = t1.sender_id
          AND t1.amount > 10000
          AND t2.amount > 10000
          AND t3.amount > 10000
    """
    c.execute(query)
    expected_ids = sorted([row[0] for row in c.fetchall()])
    conn.close()

    # Read the actual output
    with open(csv_path, 'r') as f:
        lines = f.read().splitlines()

    actual_ids = []
    for line in lines:
        line = line.strip()
        if line:
            try:
                actual_ids.append(int(line))
            except ValueError:
                pytest.fail(f"Invalid non-integer value found in CSV: {line}")

    assert actual_ids == expected_ids, f"Expected flagged entities {expected_ids}, but got {actual_ids}."

def test_database_indexes():
    db_path = '/home/user/financial_graph.db'
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Get all indexes for the transactions table
    c.execute("PRAGMA index_list('transactions');")
    indexes = c.fetchall()

    # Filter out auto-generated indexes (like sqlite_autoindex)
    user_indexes = [idx for idx in indexes if not idx[1].startswith('sqlite_')]

    conn.close()

    assert len(user_indexes) >= 2, f"Expected at least 2 user-created indexes on the 'transactions' table, but found {len(user_indexes)}."
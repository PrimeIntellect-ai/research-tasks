# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/audit.db"
SCRIPT_PATH = "/home/user/find_ring.sh"
OUTPUT_PATH = "/home/user/deadlock_cycle.txt"

def get_expected_cycle():
    """Derive the expected cycle directly from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
        SELECT t1.tx_id, t2.tx_id, t3.tx_id
        FROM transfers t1
        JOIN transfers t2 ON t1.receiver_id = t2.sender_id
        JOIN transfers t3 ON t2.receiver_id = t3.sender_id
        WHERE t3.receiver_id = t1.sender_id;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) > 0, "No cycle of length 3 found in the database."

    # Each cycle of length 3 will appear 3 times in the results (shifted).
    # We take the first one, sort its tx_ids, and return as comma-separated string.
    cycle_tx_ids = sorted(list(rows[0]))
    return ",".join(str(tx) for tx in cycle_tx_ids)

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script file {SCRIPT_PATH} is missing."

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."

def test_output_content():
    expected_content = get_expected_cycle()

    with open(OUTPUT_PATH, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {OUTPUT_PATH} is incorrect. Expected '{expected_content}', got '{content}'."
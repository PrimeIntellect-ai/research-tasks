# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/network_backup.db"
OUTPUT_FILE = "/home/user/recovery_path.txt"

def test_database_indices_repaired():
    """Verify that the corrupted index is dropped and the new covering index is created."""
    assert os.path.isfile(DB_PATH), f"Database file missing: {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verify corrupted index is dropped
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_corrupted_source'")
    assert cursor.fetchone() is None, "The corrupted index 'idx_corrupted_source' was not dropped."

    # Verify new covering index is created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_edges_covering'")
    assert cursor.fetchone() is not None, "The new index 'idx_edges_covering' was not created."

    # Verify the columns of the new index
    cursor.execute("PRAGMA index_info('idx_edges_covering')")
    index_info = cursor.fetchall()

    # index_info returns rows like: (seqno, cid, name)
    # We expect the columns to be 'source', 'target', 'cost' in that order
    columns = [row[2] for row in index_info]
    expected_columns = ['source', 'target', 'cost']

    assert columns == expected_columns, (
        f"Index 'idx_edges_covering' does not cover the correct columns in the correct order. "
        f"Expected {expected_columns}, found {columns}."
    )

    conn.close()

def test_recovery_path_file():
    """Verify that the recovery path file exists and contains the correct shortest path."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file missing: {OUTPUT_FILE}"

    with open(OUTPUT_FILE, 'r') as f:
        content = f.read().strip()

    expected_content = "Path: NODE_START,N2,N3,NODE_END | Cost: 9"
    assert content == expected_content, (
        f"Incorrect content in {OUTPUT_FILE}.\n"
        f"Expected: '{expected_content}'\n"
        f"Found: '{content}'"
    )
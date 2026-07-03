# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/backups.db'
JSON_PATH = '/home/user/summary.json'

def test_summary_json_exists():
    assert os.path.exists(JSON_PATH), f"The output file {JSON_PATH} was not created."
    assert os.path.isfile(JSON_PATH), f"The path {JSON_PATH} is not a file."

def test_summary_json_content():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Calculate expected chain 1 total size
    cursor.execute("""
        WITH RECURSIVE chain AS (
            SELECT backup_id, size_bytes FROM backups WHERE backup_id = 1
            UNION ALL
            SELECT b.backup_id, b.size_bytes FROM backups b
            INNER JOIN chain c ON b.parent_id = c.backup_id
        )
        SELECT SUM(size_bytes) FROM chain;
    """)
    expected_chain_1_size = cursor.fetchone()[0]

    # Calculate expected largest per job
    cursor.execute("""
        WITH ranked AS (
            SELECT backup_id, job_name, size_bytes,
                   ROW_NUMBER() OVER (PARTITION BY job_name ORDER BY size_bytes DESC, backup_id DESC) as rn
            FROM backups
        )
        SELECT job_name, backup_id FROM ranked WHERE rn = 1;
    """)
    expected_largest_per_job = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()

    # Load user JSON
    try:
        with open(JSON_PATH, 'r') as f:
            user_summary = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse {JSON_PATH} as valid JSON: {e}")

    # Verify structure and values
    assert "chain_1_total_size" in user_summary, "Key 'chain_1_total_size' is missing in the JSON."
    assert "largest_per_job" in user_summary, "Key 'largest_per_job' is missing in the JSON."

    assert user_summary["chain_1_total_size"] == expected_chain_1_size, \
        f"Expected chain_1_total_size to be {expected_chain_1_size}, but got {user_summary['chain_1_total_size']}."

    assert user_summary["largest_per_job"] == expected_largest_per_job, \
        f"Expected largest_per_job to be {expected_largest_per_job}, but got {user_summary['largest_per_job']}."
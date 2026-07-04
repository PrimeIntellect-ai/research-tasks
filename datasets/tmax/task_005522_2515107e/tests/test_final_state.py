# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/backup_catalog.db'
JSON_PATH = '/home/user/chain_sizes.json'
PLAN_PATH = '/home/user/query_plan.txt'

def get_expected_chain_sizes(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''
        WITH RECURSIVE backup_chain AS (
            SELECT backup_id, backup_id AS root_id, size_bytes
            FROM backups
            WHERE parent_id IS NULL AND status = 'success'

            UNION ALL

            SELECT b.backup_id, c.root_id, b.size_bytes
            FROM backups b
            JOIN backup_chain c ON b.parent_id = c.backup_id
            WHERE b.status = 'success'
        )
        SELECT root_id, SUM(size_bytes)
        FROM backup_chain
        GROUP BY root_id
    ''')
    res = {row[0]: row[1] for row in cur.fetchall()}
    conn.close()
    return res

def test_index_created():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} missing."
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='backups'")
    indexes = cur.fetchall()

    has_parent_id_index = False
    for (idx_name,) in indexes:
        if idx_name.startswith('sqlite_autoindex'):
            continue
        cur.execute(f"PRAGMA index_info({idx_name})")
        columns = [row[2] for row in cur.fetchall()]
        if 'parent_id' in columns:
            has_parent_id_index = True
            break

    conn.close()
    assert has_parent_id_index, "No secondary index covering 'parent_id' was created on the backups table."

def test_chain_sizes_json():
    assert os.path.exists(JSON_PATH), f"Output file {JSON_PATH} does not exist."

    with open(JSON_PATH, 'r') as f:
        try:
            actual_sizes = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    expected_sizes = get_expected_chain_sizes(DB_PATH)

    # Convert actual keys/values to standard types to avoid mismatch
    actual_sizes = {str(k): int(v) for k, v in actual_sizes.items()}

    assert actual_sizes == expected_sizes, "The calculated chain sizes in the JSON file do not match the expected values."

def test_query_plan_exists_and_uses_index():
    assert os.path.exists(PLAN_PATH), f"Query plan file {PLAN_PATH} does not exist."

    with open(PLAN_PATH, 'r') as f:
        plan_text = f.read().upper()

    assert "INDEX" in plan_text, "The query plan does not seem to indicate index usage for the backups table."
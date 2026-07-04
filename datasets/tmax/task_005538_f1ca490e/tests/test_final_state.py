# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/backups.db'
PLAN_PATH = '/home/user/restoration_plan.json'

def get_expected_chain():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find the most recent FULL backup for prod_payments
    cursor.execute("""
        SELECT id, backup_type, size_bytes
        FROM backup_catalog
        WHERE db_name = 'prod_payments' AND backup_type = 'FULL'
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    full_backup = cursor.fetchone()
    if not full_backup:
        conn.close()
        return []

    chain = []
    current_id = full_backup['id']
    cumulative_size = 0

    # Add FULL backup
    cumulative_size += full_backup['size_bytes']
    chain.append({
        "backup_id": full_backup['id'],
        "backup_type": full_backup['backup_type'],
        "size_bytes": full_backup['size_bytes'],
        "cumulative_size_bytes": cumulative_size
    })

    # Find descendants
    while True:
        cursor.execute("""
            SELECT id, backup_type, size_bytes
            FROM backup_catalog
            WHERE parent_id = ? AND db_name = 'prod_payments'
            ORDER BY timestamp ASC
        """, (current_id,))
        children = cursor.fetchall()
        if not children:
            break

        # Assume linear chain for simplicity based on the problem description
        child = children[0]
        cumulative_size += child['size_bytes']
        chain.append({
            "backup_id": child['id'],
            "backup_type": child['backup_type'],
            "size_bytes": child['size_bytes'],
            "cumulative_size_bytes": cumulative_size
        })
        current_id = child['id']

    conn.close()
    return chain

def test_restoration_plan_exists():
    assert os.path.exists(PLAN_PATH), f"The file {PLAN_PATH} was not created."
    assert os.path.isfile(PLAN_PATH), f"The path {PLAN_PATH} is not a file."

def test_restoration_plan_content():
    assert os.path.exists(PLAN_PATH), "Cannot test content because file is missing."

    with open(PLAN_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {PLAN_PATH} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output must be a list of objects."

    expected_chain = get_expected_chain()

    assert len(data) == len(expected_chain), f"Expected {len(expected_chain)} items in the restoration plan, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_chain)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."

        required_keys = {"backup_id", "backup_type", "size_bytes", "cumulative_size_bytes"}
        missing_keys = required_keys - actual.keys()
        assert not missing_keys, f"Item at index {i} is missing required keys: {missing_keys}"

        assert actual["backup_id"] == expected["backup_id"], f"Item {i} backup_id mismatch: expected {expected['backup_id']}, got {actual['backup_id']}"
        assert actual["backup_type"] == expected["backup_type"], f"Item {i} backup_type mismatch: expected {expected['backup_type']}, got {actual['backup_type']}"
        assert actual["size_bytes"] == expected["size_bytes"], f"Item {i} size_bytes mismatch: expected {expected['size_bytes']}, got {actual['size_bytes']}"
        assert actual["cumulative_size_bytes"] == expected["cumulative_size_bytes"], f"Item {i} cumulative_size_bytes mismatch: expected {expected['cumulative_size_bytes']}, got {actual['cumulative_size_bytes']}"
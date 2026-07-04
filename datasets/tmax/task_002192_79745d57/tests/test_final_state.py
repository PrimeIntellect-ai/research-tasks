# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/backups.db"
JSON_PATH = "/home/user/chain_summary.json"

def test_index_created():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_backups_parent';"
    )
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Index 'idx_backups_parent' was not created in the database."
    assert result[0] == 'idx_backups_parent', "Index name does not match expected."

def test_json_output():
    assert os.path.exists(JSON_PATH), f"Output JSON file {JSON_PATH} is missing."

    with open(JSON_PATH, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} does not contain valid JSON.")

    assert isinstance(actual_data, list), "JSON output should be a list of objects."

    # Compute expected data from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, parent_id, size_bytes FROM backups")
    rows = cursor.fetchall()
    conn.close()

    # Build a quick lookup
    by_id = {row[0]: row for row in rows}
    by_parent = {}
    for row in rows:
        pid = row[1]
        if pid not in by_parent:
            by_parent[pid] = []
        by_parent[pid].append(row[0])

    expected_data = []
    current_id = 'full_alpha'
    depth = 0
    running_total = 0

    while current_id:
        if current_id not in by_id:
            break
        node = by_id[current_id]
        size_bytes = node[2]
        running_total += size_bytes

        expected_data.append({
            "backup_id": current_id,
            "depth": depth,
            "size_bytes": size_bytes,
            "running_total_bytes": running_total
        })

        children = by_parent.get(current_id, [])
        if children:
            # The alpha chain is strictly linear in the setup
            current_id = children[0]
            depth += 1
        else:
            current_id = None

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} items in JSON, but found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get("backup_id") == expected["backup_id"], f"Mismatch at index {i}: expected backup_id {expected['backup_id']} but got {actual.get('backup_id')}."
        assert actual.get("depth") == expected["depth"], f"Mismatch at index {i}: expected depth {expected['depth']} but got {actual.get('depth')}."
        assert actual.get("size_bytes") == expected["size_bytes"], f"Mismatch at index {i}: expected size_bytes {expected['size_bytes']} but got {actual.get('size_bytes')}."
        assert actual.get("running_total_bytes") == expected["running_total_bytes"], f"Mismatch at index {i}: expected running_total_bytes {expected['running_total_bytes']} but got {actual.get('running_total_bytes')}."
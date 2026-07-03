# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"File {results_path} is missing."
    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    expected = [
        {"root_id": 1, "total_bytes": 10750},
        {"root_id": 4, "total_bytes": 21000},
        {"root_id": 6, "total_bytes": 5300}
    ]

    # Sort both to ensure strict comparison regardless of order
    data_sorted = sorted(data, key=lambda x: x.get("root_id", 0))
    expected_sorted = sorted(expected, key=lambda x: x["root_id"])

    assert data_sorted == expected_sorted, f"Data in {results_path} does not match expected output."

def test_plan_before():
    plan_before_path = "/home/user/plan_before.txt"
    assert os.path.isfile(plan_before_path), f"File {plan_before_path} is missing."
    with open(plan_before_path, 'r') as f:
        content = f.read().upper()

    assert "SCAN" in content, f"Expected 'SCAN' in {plan_before_path}, indicating a full table scan before optimization."
    assert "BACKUP_JOBS" in content, f"Expected table 'backup_jobs' to be mentioned in {plan_before_path}."

def test_plan_after():
    plan_after_path = "/home/user/plan_after.txt"
    assert os.path.isfile(plan_after_path), f"File {plan_after_path} is missing."
    with open(plan_after_path, 'r') as f:
        content = f.read().upper()

    assert "SEARCH" in content, f"Expected 'SEARCH' in {plan_after_path}, indicating an index was used after optimization."
    assert "BACKUP_JOBS" in content, f"Expected table 'backup_jobs' to be mentioned in {plan_after_path}."

def test_index_created():
    db_path = "/home/user/backups.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if there is an index on parent_id
    cursor.execute("PRAGMA index_list('backup_jobs');")
    indexes = cursor.fetchall()

    has_parent_id_index = False
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        columns = cursor.fetchall()
        # columns format: (seqno, cid, name)
        if any(col[2] == 'parent_id' for col in columns):
            has_parent_id_index = True
            break

    conn.close()

    assert has_parent_id_index, "No index found on the 'parent_id' column of the 'backup_jobs' table."
# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/backups.db'
RESULTS_PATH = '/home/user/analysis_results.json'

def test_indexes_created():
    """Verify that appropriate indexes were created on the backup_jobs table."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA index_list('backup_jobs');")
    indexes = cursor.fetchall()

    assert len(indexes) > 0, "No indexes were created on the 'backup_jobs' table."

    indexed_columns = []
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}');")
        columns = [row[2] for row in cursor.fetchall()]
        indexed_columns.append(columns)

    conn.close()

    # We expect an index that helps with parent_backup_id
    has_parent_idx = any('parent_backup_id' in cols for cols in indexed_columns)
    assert has_parent_idx, "Missing index on 'parent_backup_id' for hierarchical queries."

    # We expect an index that helps with db_name and start_time
    has_window_idx = any('db_name' in cols and 'start_time' in cols for cols in indexed_columns) or \
                     (any('db_name' in cols for cols in indexed_columns) and any('start_time' in cols for cols in indexed_columns))
    assert has_window_idx, "Missing index on 'db_name' and/or 'start_time' for window functions."

def test_analysis_results_file_exists():
    """Verify that the JSON results file was created."""
    assert os.path.exists(RESULTS_PATH), f"Results file missing at {RESULTS_PATH}"
    assert os.path.isfile(RESULTS_PATH), f"Expected a file at {RESULTS_PATH}, but found a directory"

def test_analysis_results_content():
    """Verify the content of the JSON results file matches the expected logic."""
    with open(RESULTS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {RESULTS_PATH} is not valid JSON.")

    assert isinstance(data, list), "JSON root must be an array."
    assert len(data) == 6, f"Expected 6 backup chains, found {len(data)}."

    # Create a dictionary for easy lookup by root_backup_id
    results_by_id = {item.get('root_backup_id'): item for item in data}

    expected_results = {
        1: {"db_name": "auth_db", "total_chain_size": 125, "is_anomalous": False},
        4: {"db_name": "auth_db", "total_chain_size": 130, "is_anomalous": False},
        6: {"db_name": "auth_db", "total_chain_size": 300, "is_anomalous": True},
        8: {"db_name": "users_db", "total_chain_size": 500, "is_anomalous": False},
        9: {"db_name": "users_db", "total_chain_size": 550, "is_anomalous": False},
        10: {"db_name": "users_db", "total_chain_size": 600, "is_anomalous": False}
    }

    for expected_id, expected_data in expected_results.items():
        assert expected_id in results_by_id, f"Missing root_backup_id {expected_id} in results."

        actual_data = results_by_id[expected_id]

        # Check required keys
        for key in ["db_name", "total_chain_size", "is_anomalous"]:
            assert key in actual_data, f"Missing key '{key}' in result for root_backup_id {expected_id}."

        assert actual_data["db_name"] == expected_data["db_name"], \
            f"Mismatch in db_name for root_backup_id {expected_id}: expected {expected_data['db_name']}, got {actual_data['db_name']}"

        assert actual_data["total_chain_size"] == expected_data["total_chain_size"], \
            f"Mismatch in total_chain_size for root_backup_id {expected_id}: expected {expected_data['total_chain_size']}, got {actual_data['total_chain_size']}"

        # Handle boolean or integer representation of boolean (0/1)
        actual_anomalous = bool(actual_data["is_anomalous"])
        assert actual_anomalous == expected_data["is_anomalous"], \
            f"Mismatch in is_anomalous for root_backup_id {expected_id}: expected {expected_data['is_anomalous']}, got {actual_anomalous}"
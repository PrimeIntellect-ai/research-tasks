# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = '/home/user/etl_lineage.db'
RESULT_PATH = '/home/user/pipeline_result.json'

def test_result_file_exists_and_valid():
    assert os.path.exists(RESULT_PATH), f"Result file {RESULT_PATH} does not exist."
    assert os.path.isfile(RESULT_PATH), f"Path {RESULT_PATH} is not a file."

    with open(RESULT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULT_PATH} does not contain valid JSON.")

    assert "created_indexes" in data, "JSON missing 'created_indexes' key."
    assert "query_plan" in data, "JSON missing 'query_plan' key."
    assert "min_transfer_cost" in data, "JSON missing 'min_transfer_cost' key."

def test_min_transfer_cost():
    with open(RESULT_PATH, 'r') as f:
        data = json.load(f)

    assert data["min_transfer_cost"] == 40, f"Expected min_transfer_cost to be 40, got {data['min_transfer_cost']}"

def test_created_indexes_info():
    with open(RESULT_PATH, 'r') as f:
        data = json.load(f)

    created_indexes = data["created_indexes"]
    assert isinstance(created_indexes, list), "'created_indexes' must be a list."
    assert len(created_indexes) > 0, "'created_indexes' list is empty. Expected at least one index."

def test_query_plan_indicates_index_usage():
    with open(RESULT_PATH, 'r') as f:
        data = json.load(f)

    query_plan = data["query_plan"]
    assert isinstance(query_plan, str), "'query_plan' must be a string."

    plan_upper = query_plan.upper()
    assert "SEARCH" in plan_upper or "INDEX" in plan_upper, "query_plan does not seem to indicate index usage (missing 'SEARCH' or 'INDEX')."

def test_database_has_correct_index():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Get all indexes for the dependencies table
        cursor.execute("PRAGMA index_list('dependencies');")
        indexes = cursor.fetchall()

        user_indexes = [idx[1] for idx in indexes if not idx[1].startswith('sqlite_autoindex')]
        assert len(user_indexes) > 0, "No user-created indexes found on the 'dependencies' table."

        has_source_task_index = False
        for idx_name in user_indexes:
            cursor.execute(f"PRAGMA index_info('{idx_name}');")
            columns = cursor.fetchall()
            if columns and columns[0][2] == 'source_task':
                has_source_task_index = True
                break

        assert has_source_task_index, "No index found where the first column is 'source_task'."
    finally:
        conn.close()
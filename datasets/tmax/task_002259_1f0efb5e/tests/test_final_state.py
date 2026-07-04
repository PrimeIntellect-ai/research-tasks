# test_final_state.py

import os
import json
import sqlite3
import pytest

DB_PATH = '/home/user/backup_metadata.db'
OUTPUT_JSON_PATH = '/home/user/failed_downstream.json'

def test_json_output_correct():
    assert os.path.isfile(OUTPUT_JSON_PATH), f"Output file {OUTPUT_JSON_PATH} does not exist."

    with open(OUTPUT_JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_JSON_PATH} does not contain valid JSON.")

    expected_data = ["export_job_s3", "table_orders", "view_daily_sales"]

    assert isinstance(data, list), "JSON output should be a list."
    assert data == expected_data, f"JSON output {data} does not match expected {expected_data}."

def test_database_indexes_created():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check indexes on edges table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges';")
    edges_indexes = cursor.fetchall()
    assert len(edges_indexes) > 0, "No indexes found on the 'edges' table."

    # Check indexes on backup_runs table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='backup_runs';")
    backup_runs_indexes = cursor.fetchall()
    assert len(backup_runs_indexes) > 0, "No indexes found on the 'backup_runs' table."

    conn.close()
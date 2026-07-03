# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = '/home/user/graph_backup.db'
RESULTS_PATH = '/home/user/results.json'
SCRIPT_PATH = '/home/user/extract.py'

def test_index_created():
    assert os.path.exists(DB_PATH), f"Database missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name='idx_edges_target';")
    idx = cur.fetchone()
    conn.close()

    assert idx is not None, "Index 'idx_edges_target' was not created."
    assert idx[1] == 'edges', f"Index 'idx_edges_target' is on the wrong table: {idx[1]} instead of edges."

def test_extract_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Python script missing at {SCRIPT_PATH}"

def test_results_json():
    assert os.path.exists(RESULTS_PATH), f"Results JSON missing at {RESULTS_PATH}"

    with open(RESULTS_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULTS_PATH} is not valid JSON")

    expected = [
        {"source_name": "auth_service", "source_status": "active"},
        {"source_name": "background_worker", "source_status": "active"},
        {"source_name": "web_api", "source_status": "active"}
    ]

    assert isinstance(data, list), "JSON root must be a list."
    assert len(data) == len(expected), f"Expected {len(expected)} items, got {len(data)}."

    # Check if exactly equal to expected (including order, uniqueness, and exact keys)
    assert data == expected, f"JSON output does not match expected results. Expected: {expected}, Got: {data}"
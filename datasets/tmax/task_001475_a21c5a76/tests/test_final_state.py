# test_final_state.py

import os
import sqlite3
import subprocess
import pytest

DB_PATH = "/home/user/etl_graph.db"
SCRIPT_PATH = "/home/user/find_downstream.sh"
QUERY_PLAN_PATH = "/home/user/query_plan.txt"

def test_index_created():
    """Test that the index idx_dep_source was created on dependencies(source_id)."""
    assert os.path.isfile(DB_PATH), f"Database file not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if index exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_dep_source';")
    assert cursor.fetchone() is not None, "Index 'idx_dep_source' does not exist."

    # Check if index is on source_id
    cursor.execute("PRAGMA index_info('idx_dep_source');")
    index_info = cursor.fetchall()
    assert len(index_info) >= 1, "Index 'idx_dep_source' has no columns."

    # Pragma index_info returns: seqno, cid, name
    column_names = [info[2] for info in index_info]
    assert column_names[0] == 'source_id', f"Index 'idx_dep_source' is not on 'source_id' column. Found: {column_names}"

    conn.close()

def test_script_exists_and_executable():
    """Test that the script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable."

def test_script_output_extract_users():
    """Test the output of the script for 'extract_users'."""
    expected_output = [
        "aggregate_metrics",
        "generate_reports",
        "join_data",
        "load_warehouse",
        "send_alerts",
        "transform_users"
    ]

    result = subprocess.run([SCRIPT_PATH, "extract_users"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    assert output_lines == expected_output, f"Expected {expected_output}, got {output_lines}"

def test_script_output_extract_orders():
    """Test the output of the script for 'extract_orders' to ensure it handles arguments properly."""
    expected_output = [
        "aggregate_metrics",
        "generate_reports",
        "join_data",
        "load_warehouse",
        "send_alerts",
        "transform_orders"
    ]

    result = subprocess.run([SCRIPT_PATH, "extract_orders"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    output_lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
    assert output_lines == expected_output, f"Expected {expected_output}, got {output_lines}"

def test_query_plan_output():
    """Test that query_plan.txt exists and references the index."""
    assert os.path.isfile(QUERY_PLAN_PATH), f"Query plan file not found at {QUERY_PLAN_PATH}"

    with open(QUERY_PLAN_PATH, 'r') as f:
        content = f.read()

    assert "idx_dep_source" in content, "Query plan does not reference 'idx_dep_source'."
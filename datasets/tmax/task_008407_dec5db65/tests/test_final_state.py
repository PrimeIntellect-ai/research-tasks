# test_final_state.py

import os
import sqlite3
import pytest
import re

DB_PATH = "/home/user/system_graph.db"
SCHEMA_PATH = "/home/user/schema.txt"
SCRIPT_PATH = "/home/user/graph_metrics.py"
METRICS_PATH = "/home/user/node_42_metrics.txt"

def test_schema_txt_exists_and_correct():
    """Verify that schema.txt contains the correct CREATE TABLE statement."""
    assert os.path.isfile(SCHEMA_PATH), f"{SCHEMA_PATH} does not exist."
    with open(SCHEMA_PATH, 'r') as f:
        content = f.read().strip().lower()

    # Normalize whitespace
    content = re.sub(r'\s+', ' ', content)

    assert "create table hidden_rels" in content, "schema.txt does not contain 'CREATE TABLE hidden_rels'"
    assert "u integer" in content, "schema.txt does not define column 'u' as INTEGER"
    assert "v integer" in content, "schema.txt does not define column 'v' as INTEGER"

def test_indexes_created():
    """Verify that idx_source and idx_dest indexes are created on hidden_rels."""
    assert os.path.isfile(DB_PATH), f"Database file not found at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index' AND name IN ('idx_source', 'idx_dest');")
    indexes = cursor.fetchall()
    conn.close()

    index_dict = {name: tbl_name for name, tbl_name in indexes}

    assert 'idx_source' in index_dict, "Index 'idx_source' was not created."
    assert index_dict['idx_source'] == 'hidden_rels', "Index 'idx_source' should be on table 'hidden_rels'."

    assert 'idx_dest' in index_dict, "Index 'idx_dest' was not created."
    assert index_dict['idx_dest'] == 'hidden_rels', "Index 'idx_dest' should be on table 'hidden_rels'."

def test_graph_metrics_script_parameterized():
    """Verify that graph_metrics.py exists and uses parameterized queries."""
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} does not exist."
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    # Check for parameterization markers like ? or :name
    # A simple check for '?' is usually sufficient for sqlite3 parameterization
    assert '?' in content or re.search(r':\w+', content), "graph_metrics.py does not appear to use parameterized queries (missing '?' or named parameters)."

def test_node_42_metrics_correct():
    """Verify that node_42_metrics.txt contains the correct degree calculation."""
    assert os.path.isfile(METRICS_PATH), f"{METRICS_PATH} does not exist."

    # Calculate truth
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM hidden_rels WHERE u = 42 OR v = 42;")
    expected_degree = cursor.fetchone()[0]
    conn.close()

    with open(METRICS_PATH, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"{METRICS_PATH} should contain only an integer."
    actual_degree = int(content)

    assert actual_degree == expected_degree, f"Expected degree {expected_degree}, but found {actual_degree} in {METRICS_PATH}."
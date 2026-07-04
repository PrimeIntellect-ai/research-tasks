# test_final_state.py

import os
import sqlite3
import pytest

def test_analyze_script_exists():
    assert os.path.isfile('/home/user/analyze.sh'), "/home/user/analyze.sh script is missing"

def test_graph_db_exists():
    assert os.path.isfile('/home/user/graph.db'), "/home/user/graph.db is missing"

def test_projected_edges_table_exists():
    db_path = '/home/user/graph.db'
    assert os.path.isfile(db_path), f"{db_path} is missing"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projected_edges';")
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Table 'projected_edges' not found in /home/user/graph.db"

def test_idx_source_exists():
    db_path = '/home/user/graph.db'
    assert os.path.isfile(db_path), f"{db_path} is missing"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_source';")
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Index 'idx_source' not found in /home/user/graph.db"

def test_top_nodes_txt():
    file_path = '/home/user/top_nodes.txt'
    assert os.path.isfile(file_path), f"{file_path} is missing"

    expected_content = """Handle: Alice, OutDegree: 3
Handle: Bob, OutDegree: 2
Handle: Charlie, OutDegree: 1"""

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} does not match expected output.\nExpected:\n{expected_content}\nActual:\n{content}"
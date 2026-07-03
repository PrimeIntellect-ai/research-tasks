# test_final_state.py

import os
import sqlite3
import pytest

def test_db_updated_correctly():
    db_path = "/home/user/graph.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT id, weight FROM nodes ORDER BY id")
    rows = c.fetchall()
    conn.close()

    weights = {row[0]: row[1] for row in rows}

    # Base weights: ROOT=10, A=20, B=30, C=40, D=50, E=60
    # Updates: A, B, C, D get +5 and +10 (+15 total)
    expected_weights = {
        'ROOT': 10,
        'A': 35,
        'B': 45,
        'C': 55,
        'D': 65,
        'E': 60
    }

    for node, expected in expected_weights.items():
        assert weights.get(node) == expected, f"Node {node} expected weight {expected}, got {weights.get(node)}"

def test_python_script_fixed():
    script_path = "/home/user/concurrent_update.py"
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    # Check for parameterized queries
    assert "?" in content, "The script should use parameterized queries (e.g., '?') instead of string formatting."
    assert "f\"UPDATE" not in content and "f'UPDATE" not in content, "The script should not use f-strings for the UPDATE query."

    # Check for sorting
    assert "sort" in content, "The script should sort the nodes_to_update list before iterating to prevent deadlocks."

def test_sql_script_exists_and_recursive():
    sql_path = "/home/user/analyze.sql"
    assert os.path.isfile(sql_path), f"SQL script {sql_path} is missing."

    with open(sql_path, 'r') as f:
        content = f.read().upper()

    assert "WITH RECURSIVE" in content or "WITH " in content, "The SQL script should use a Recursive Common Table Expression (CTE)."
    assert "ROOT" in content, "The SQL script should start from the 'ROOT' node."

def test_result_file():
    result_path = "/home/user/root_total_weight.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} is missing."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content == "270", f"Expected the total weight to be 270, but got '{content}'."
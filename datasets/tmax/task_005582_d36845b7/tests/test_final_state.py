# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_project_directory_exists():
    project_path = '/home/user/graph_analyzer'
    assert os.path.isdir(project_path), f"Project directory {project_path} does not exist."
    assert os.path.isfile(os.path.join(project_path, 'Cargo.toml')), "Cargo.toml not found in the project directory."

def test_results_json_correct():
    results_path = '/home/user/results.json'
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    with open(results_path, 'r', encoding='utf-8') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    expected_results = [
        {"destination": "N003", "weight": 6.0},
        {"destination": "N005", "weight": 5.0},
        {"destination": "N003", "weight": 4.0}
    ]

    assert results == expected_results, f"Contents of {results_path} do not match the expected top 3 results."

def test_database_exists_and_indexes_created():
    db_path = '/home/user/graph.db'
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check for indexes on the edges table
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='index' AND tbl_name='edges';")
    index_count = cursor.fetchone()[0]

    assert index_count > 0, "No indexes were created on the 'edges' table."

    conn.close()

def test_two_hop_paths_table_exists_and_populated():
    db_path = '/home/user/graph.db'
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='two_hop_paths';")
    table_exists = cursor.fetchone()
    assert table_exists is not None, "Table 'two_hop_paths' does not exist in the database."

    # Check if table is populated
    cursor.execute("SELECT count(*) FROM two_hop_paths;")
    row_count = cursor.fetchone()[0]
    assert row_count > 0, "Table 'two_hop_paths' is empty."

    # Check schema roughly
    cursor.execute("PRAGMA table_info(two_hop_paths);")
    columns = [row[1] for row in cursor.fetchall()]
    assert "start_node" in columns, "Column 'start_node' missing from 'two_hop_paths'."
    assert "end_node" in columns, "Column 'end_node' missing from 'two_hop_paths'."
    assert "total_weight" in columns, "Column 'total_weight' missing from 'two_hop_paths'."

    conn.close()
# test_final_state.py

import os
import sqlite3
import re

def test_optimize_sql():
    sql_file = '/home/user/optimize.sql'
    assert os.path.exists(sql_file), f"{sql_file} does not exist."

    with open(sql_file, 'r') as f:
        content = f.read().lower()

    # Check that there is a CREATE INDEX statement on Edges(source_id)
    assert 'create index' in content, f"No CREATE INDEX statement found in {sql_file}."
    assert 'edges' in content and 'source_id' in content, f"Index does not appear to be on Edges(source_id) in {sql_file}."

def test_database_has_index():
    db_file = '/home/user/graph.db'
    assert os.path.exists(db_file), f"{db_file} does not exist."

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query sqlite_master for the index
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='Edges'")
    indices = cursor.fetchall()

    has_source_id_index = False
    for (sql,) in indices:
        if sql and 'source_id' in sql.lower():
            has_source_id_index = True
            break

    conn.close()
    assert has_source_id_index, "The graph.db does not contain an index on Edges(source_id). Did you execute optimize.sql?"

def test_pipeline_executable_exists():
    exe_file = '/home/user/pipeline'
    assert os.path.exists(exe_file), f"Compiled executable {exe_file} does not exist."
    assert os.access(exe_file, os.X_OK), f"{exe_file} is not executable."

def test_final_nodes_csv():
    csv_file = '/home/user/final_nodes.csv'
    assert os.path.exists(csv_file), f"{csv_file} does not exist."

    # Compute expected values using python sqlite3
    db_file = '/home/user/graph.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    query = """
        WITH RECURSIVE traverse(id) AS (
          SELECT target_id FROM Edges WHERE source_id = ? 
          UNION 
          SELECT Edges.target_id FROM Edges JOIN traverse ON Edges.source_id = traverse.id
        ) 
        SELECT SUM(weight) FROM Edges WHERE source_id IN traverse;
    """

    expected_values = {}
    for node_id in range(1, 6):
        cursor.execute(query, (node_id,))
        res = cursor.fetchone()[0]
        expected_values[node_id] = res if res is not None else 0

    conn.close()

    # Read the CSV
    with open(csv_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected 5 lines in {csv_file}, but got {len(lines)}."

    parsed_csv = {}
    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Invalid CSV format: '{line}'"
        node_id, val = int(parts[0]), int(parts[1])
        parsed_csv[node_id] = val

    for node_id in range(1, 6):
        assert node_id in parsed_csv, f"Node {node_id} missing from {csv_file}."
        assert parsed_csv[node_id] == expected_values[node_id], f"Node {node_id} has incorrect value. Expected {expected_values[node_id]}, got {parsed_csv[node_id]}."

def test_pipeline_cpp_deadlock_fix():
    cpp_file = '/home/user/pipeline.cpp'
    assert os.path.exists(cpp_file), f"{cpp_file} does not exist."

    with open(cpp_file, 'r') as f:
        content = f.read()

    # Check if BEGIN was changed to something that prevents deadlock like BEGIN IMMEDIATE or BEGIN EXCLUSIVE
    # or if some mutex was added.
    # The default BEGIN causes deadlocks, so it should not be just "BEGIN;" anymore.
    # We will check that they either use IMMEDIATE/EXCLUSIVE or std::mutex.
    has_immediate = 'BEGIN IMMEDIATE' in content.upper()
    has_exclusive = 'BEGIN EXCLUSIVE' in content.upper()
    has_mutex = 'std::mutex' in content or 'std::lock_guard' in content

    assert has_immediate or has_exclusive or has_mutex, "pipeline.cpp does not appear to fix the deadlock. Need to use BEGIN IMMEDIATE, BEGIN EXCLUSIVE, or a mutex."
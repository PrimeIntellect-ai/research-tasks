# test_final_state.py

import os
import sqlite3
import json
import pytest
import stat

def compute_expected_sum(db_path, json_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Find active intermediate nodes (1st hop)
    cursor.execute("""
        SELECT e.target 
        FROM edges e
        JOIN nodes n ON e.target = n.id
        WHERE e.source = 1 AND n.status = 'active'
    """)
    intermediates = [row[0] for row in cursor.fetchall()]

    if not intermediates:
        conn.close()
        return 0

    # Find 2nd hop targets
    placeholders = ','.join('?' for _ in intermediates)
    cursor.execute(f"""
        SELECT DISTINCT target 
        FROM edges 
        WHERE source IN ({placeholders})
    """, intermediates)
    target_nodes = {row[0] for row in cursor.fetchall()}
    conn.close()

    # Sum telemetry values
    with open(json_path, 'r') as f:
        telemetry_data = json.load(f)

    total_sum = sum(item.get('value', 0) for item in telemetry_data if item.get('node_id') in target_nodes)
    return total_sum

def test_result_txt_content():
    result_path = "/home/user/result.txt"
    db_path = "/home/user/graph.db"
    json_path = "/home/user/telemetry.json"

    assert os.path.isfile(result_path), f"Output file {result_path} is missing."

    expected_sum = compute_expected_sum(db_path, json_path)

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"File {result_path} must contain only an integer, got '{content}'."
    assert int(content) == expected_sum, f"Expected sum {expected_sum}, but got {content} in {result_path}."

def test_optimize_sql_exists_and_valid():
    sql_path = "/home/user/optimize.sql"
    assert os.path.isfile(sql_path), f"SQL file {sql_path} is missing."

    with open(sql_path, 'r') as f:
        content = f.read().upper()

    assert "CREATE INDEX" in content, f"File {sql_path} does not seem to contain CREATE INDEX statements."

def test_indexes_applied_to_db():
    db_path = "/home/user/graph.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_autoindex%';")
    indexes = cursor.fetchall()
    conn.close()

    assert len(indexes) > 0, "No custom indexes were found in graph.db. Ensure optimize.sql was applied."

def test_fast_query_sh_exists_and_executable():
    script_path = "/home/user/fast_query.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."
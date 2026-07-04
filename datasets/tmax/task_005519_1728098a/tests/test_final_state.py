# test_final_state.py

import os
import sqlite3
import json
import subprocess
import pytest

DB_PATH = "/home/user/audit.db"
SCRIPT_PATH = "/home/user/generate_graph.sh"
JSON_PATH = "/home/user/audit_graph.json"

def test_database_indexes():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check idx_gm_emp
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND name='idx_gm_emp';")
    row = cursor.fetchone()
    assert row is not None, "Index 'idx_gm_emp' is missing."
    sql = row[0].lower()
    assert "group_members" in sql, "Index 'idx_gm_emp' should be on the 'group_members' table."
    assert "emp_id" in sql, "Index 'idx_gm_emp' should be on the 'emp_id' column."

    # Check idx_ga_group
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND name='idx_ga_group';")
    row = cursor.fetchone()
    assert row is not None, "Index 'idx_ga_group' is missing."
    sql = row[0].lower()
    assert "group_access" in sql, "Index 'idx_ga_group' should be on the 'group_access' table."
    assert "group_id" in sql, "Index 'idx_ga_group' should be on the 'group_id' column."

    conn.close()

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_json_output():
    # Remove the output file if it exists to ensure the script generates it
    if os.path.exists(JSON_PATH):
        os.remove(JSON_PATH)

    # Execute the script
    try:
        result = subprocess.run([SCRIPT_PATH], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Script execution failed with exit code {e.returncode}.\nStderr: {e.stderr}")

    assert os.path.exists(JSON_PATH), f"Script did not generate the expected output file at {JSON_PATH}."

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON output: {e}")

    assert "nodes" in data, "JSON output is missing the 'nodes' array."
    assert "edges" in data, "JSON output is missing the 'edges' array."

    nodes = {n.get("id"): n for n in data["nodes"]}
    edges = {(e.get("source"), e.get("target"), e.get("relation")) for e in data["edges"]}

    expected_nodes_ids = {'emp_1', 'emp_2', 'emp_3', 'sys_50', 'sys_51', 'sys_52'}
    assert set(nodes.keys()) == expected_nodes_ids, f"Expected node IDs {expected_nodes_ids}, but got {set(nodes.keys())}."

    # Validate node types and names
    assert nodes['emp_1'] == {"id": "emp_1", "type": "employee", "name": "Alice"}
    assert nodes['emp_2'] == {"id": "emp_2", "type": "employee", "name": "Bob"}
    assert nodes['emp_3'] == {"id": "emp_3", "type": "employee", "name": "Charlie"}
    assert nodes['sys_50'] == {"id": "sys_50", "type": "system", "name": "Finance"}
    assert nodes['sys_51'] == {"id": "sys_51", "type": "system", "name": "HR"}
    assert nodes['sys_52'] == {"id": "sys_52", "type": "system", "name": "IT"}

    expected_edges = {
        ('emp_1', 'sys_50', 'HAS_ACCESS'),
        ('emp_1', 'sys_51', 'HAS_ACCESS'),
        ('emp_2', 'sys_50', 'HAS_ACCESS')
    }
    assert edges == expected_edges, f"Expected edges {expected_edges}, but got {edges}."

    # Check uniqueness
    assert len(data["nodes"]) == len(nodes), "Duplicate nodes found in the JSON output."
    assert len(data["edges"]) == len(edges), "Duplicate edges found in the JSON output."
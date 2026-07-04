# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/backup_neighborhood.sh"

def test_script_exists_and_executable():
    """Verify the bash script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_script_output_node_10():
    """Run the script for node 10 and verify the output."""
    result = subprocess.run([SCRIPT_PATH, "10"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    output_file = "/home/user/backup_10.json"
    assert os.path.isfile(output_file), f"Output file {output_file} was not created"

    with open(output_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file for node 10 is not valid JSON")

    assert data.get("center_node") == 10, "center_node is incorrect"

    expected_edges = [
        {"source": 10, "target": 20, "type": "MANAGES"},
        {"source": 10, "target": 40, "type": "INVITED"},
        {"source": 30, "target": 10, "type": "REPORTS_TO"}
    ]

    expected_nodes = [
        {"id": 10, "data": '{"name": "Alice", "role": "admin"}'},
        {"id": 20, "data": '{"name": "Bob", "role": "user"}'},
        {"id": 30, "data": '{"name": "Charlie", "role": "user"}'},
        {"id": 40, "data": '{"name": "David", "role": "guest"}'}
    ]

    assert data.get("edges") == expected_edges, "Edges array is incorrect or not sorted properly for node 10"
    assert data.get("nodes") == expected_nodes, "Nodes array is incorrect or not sorted properly for node 10"

def test_script_output_node_20():
    """Run the script for node 20 to ensure it dynamically handles different inputs."""
    result = subprocess.run([SCRIPT_PATH, "20"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    output_file = "/home/user/backup_20.json"
    assert os.path.isfile(output_file), f"Output file {output_file} was not created"

    with open(output_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file for node 20 is not valid JSON")

    assert data.get("center_node") == 20, "center_node is incorrect"

    expected_edges = [
        {"source": 10, "target": 20, "type": "MANAGES"},
        {"source": 20, "target": 30, "type": "KNOWS"},
        {"source": 40, "target": 20, "type": "KNOWS"}
    ]

    expected_nodes = [
        {"id": 10, "data": '{"name": "Alice", "role": "admin"}'},
        {"id": 20, "data": '{"name": "Bob", "role": "user"}'},
        {"id": 30, "data": '{"name": "Charlie", "role": "user"}'},
        {"id": 40, "data": '{"name": "David", "role": "guest"}'}
    ]

    assert data.get("edges") == expected_edges, "Edges array is incorrect or not sorted properly for node 20"
    assert data.get("nodes") == expected_nodes, "Nodes array is incorrect or not sorted properly for node 20"
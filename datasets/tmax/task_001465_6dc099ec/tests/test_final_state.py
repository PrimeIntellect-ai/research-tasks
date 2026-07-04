# test_final_state.py
import os
import json
import subprocess
import pytest

SCRIPT_PATH = '/home/user/export_graph.py'
JSON_PATH = '/home/user/graph.json'

def test_script_exists():
    """Test that the required script exists."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_script_uses_window_function():
    """Test that the script uses an SQL Window Function."""
    with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
        content = f.read().upper()
    assert 'OVER' in content, "The script must use an SQL Window Function (e.g., OVER clause) to deduplicate citations."

def test_script_execution_and_output():
    """Test that the script executes successfully and generates the correct JSON output."""
    # Ensure a clean state for the output file
    if os.path.exists(JSON_PATH):
        os.remove(JSON_PATH)

    # Run the script with the specified arguments
    result = subprocess.run(
        ['python3', SCRIPT_PATH, '2015', '2020'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed to execute. Stderr: {result.stderr}"

    # Check if the output file was created
    assert os.path.isfile(JSON_PATH), f"Output file not found at {JSON_PATH} after running the script."

    # Parse and validate the JSON output
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} does not contain valid JSON.")

    assert "nodes" in data, "JSON output is missing the 'nodes' key."
    assert "edges" in data, "JSON output is missing the 'edges' key."

    expected_nodes = [
        {"id": 1, "title": "Paper A", "year": 2015},
        {"id": 2, "title": "Paper B", "year": 2016},
        {"id": 3, "title": "Paper C", "year": 2018}
    ]

    expected_edges = [
        {"source": 2, "target": 1, "citation_date": "2016-05-05"},
        {"source": 3, "target": 1, "citation_date": "2018-02-02"},
        {"source": 3, "target": 2, "citation_date": "2018-03-03"}
    ]

    assert data["nodes"] == expected_nodes, f"Nodes do not match expected output. Got: {data['nodes']}"
    assert data["edges"] == expected_edges, f"Edges do not match expected output. Got: {data['edges']}"
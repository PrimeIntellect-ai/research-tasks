# test_final_state.py

import os
import json
import pytest

def test_script_exists():
    script_path = '/home/user/analyze_graph.sh'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_output_json_exists():
    output_path = '/home/user/top_nodes.json'
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist. Did you run your script?"

def test_output_json_content():
    output_path = '/home/user/top_nodes.json'

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    assert isinstance(data, list), f"The JSON output should be a list, but got {type(data).__name__}."
    assert len(data) == 3, f"The JSON output should contain exactly 3 elements, but got {len(data)}."

    expected_data = [
        {"node_id": "A", "centrality": 6},
        {"node_id": "B", "centrality": 2},
        {"node_id": "C", "centrality": 2}
    ]

    for i, expected in enumerate(expected_data):
        assert data[i] == expected, f"Mismatch at index {i}. Expected {expected}, but got {data[i]}."
# test_final_state.py

import os
import json
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_pipeline_execution_and_output():
    script_path = "/home/user/pipeline.sh"
    output_path = "/home/user/top_nodes.json"

    # Remove output file if it exists to ensure we are testing a fresh run
    if os.path.exists(output_path):
        os.remove(output_path)

    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStderr: {result.stderr}"

    # Check if output file was created
    assert os.path.isfile(output_path), f"Output file {output_path} was not created by the script."

    # Read and parse JSON
    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {output_path} as JSON: {e}")

    # Validate the structure and content
    assert isinstance(data, list), "The top-level JSON structure must be a list."
    assert len(data) == 3, f"Expected exactly 3 nodes in the output, got {len(data)}."

    expected_data = [
        {
            "node": "F",
            "out_deg": 1,
            "in_deg": 0,
            "total_out": 300,
            "total_in": 0
        },
        {
            "node": "C",
            "out_deg": 2,
            "in_deg": 2,
            "total_out": 211,
            "total_in": 120
        },
        {
            "node": "A",
            "out_deg": 2,
            "in_deg": 2,
            "total_out": 150,
            "total_in": 250
        }
    ]

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Element at index {i} is not a dictionary."
        for key, expected_val in expected.items():
            assert key in actual, f"Missing key '{key}' in element at index {i}."
            assert isinstance(actual[key], type(expected_val)), f"Incorrect type for key '{key}' at index {i}. Expected {type(expected_val).__name__}, got {type(actual[key]).__name__}."
            assert actual[key] == expected_val, f"Incorrect value for key '{key}' at index {i}. Expected {expected_val}, got {actual[key]}."
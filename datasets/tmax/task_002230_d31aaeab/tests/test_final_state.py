# test_final_state.py

import os
import json
import pytest
import subprocess

C_SOURCE_PATH = "/home/user/process_graph.c"
EXEC_PATH = "/home/user/process_graph"
JSON_OUTPUT_PATH = "/home/user/valid_nodes.json"

def test_c_source_exists():
    """Test that the C source code file exists."""
    assert os.path.isfile(C_SOURCE_PATH), f"C source file missing at {C_SOURCE_PATH}"

def test_executable_exists_and_runnable():
    """Test that the compiled executable exists and is executable."""
    assert os.path.isfile(EXEC_PATH), f"Compiled executable missing at {EXEC_PATH}"
    assert os.access(EXEC_PATH, os.X_OK), f"File at {EXEC_PATH} is not executable"

def test_json_output_contents():
    """Test that the valid_nodes.json file contains the correct JSON array."""
    assert os.path.isfile(JSON_OUTPUT_PATH), f"JSON output file missing at {JSON_OUTPUT_PATH}"

    with open(JSON_OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {JSON_OUTPUT_PATH} as JSON: {e}")

    assert isinstance(data, list), "JSON output must be a list (array) of objects."

    # Sort the actual data by id to ensure order doesn't fail the test
    try:
        sorted_data = sorted(data, key=lambda x: x.get("id", 0))
    except Exception as e:
        pytest.fail(f"Failed to sort JSON data by 'id'. Ensure all objects have an integer 'id'. Error: {e}")

    expected_data = [
        {"id": 20, "title": "Valid Bridge 1"},
        {"id": 21, "title": "Valid Bridge 2"}
    ]

    assert sorted_data == expected_data, f"JSON contents do not match expected output. Got: {sorted_data}"

def test_executable_behavior(tmp_path):
    """Test that running the executable produces the correct output file."""
    # We run the executable again to ensure it actually does the job, 
    # in case the user hardcoded the JSON file.

    # Run the executable with source_id=10 and target_id=50
    result = subprocess.run([EXEC_PATH, "10", "50"], capture_output=True, text=True)
    assert result.returncode == 0, f"Executable failed with return code {result.returncode}. Stderr: {result.stderr}"

    # Check the JSON output again after running
    assert os.path.isfile(JSON_OUTPUT_PATH), f"JSON output file missing at {JSON_OUTPUT_PATH} after running executable."

    with open(JSON_OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {JSON_OUTPUT_PATH} as JSON after running executable: {e}")

    sorted_data = sorted(data, key=lambda x: x.get("id", 0))
    expected_data = [
        {"id": 20, "title": "Valid Bridge 1"},
        {"id": 21, "title": "Valid Bridge 2"}
    ]

    assert sorted_data == expected_data, f"Executable did not produce the correct JSON output. Got: {sorted_data}"
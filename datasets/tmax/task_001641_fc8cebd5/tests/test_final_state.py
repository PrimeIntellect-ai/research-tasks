# test_final_state.py

import os
import json
import pytest

def test_script_exists_and_executable():
    """Test that the bash script exists and is executable."""
    script_path = '/home/user/detect_deadlocks.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_jena_extracted():
    """Test that Apache Jena was extracted to the correct directory."""
    jena_dir = '/home/user/jena'
    assert os.path.isdir(jena_dir), f"Directory {jena_dir} does not exist."
    # Check for the sparql binary inside the extracted jena folder
    # The extraction might place it in /home/user/jena/apache-jena-4.9.0/bin/sparql or /home/user/jena/bin/sparql
    # We will just check if 'sparql' exists anywhere in the jena directory
    sparql_found = False
    for root, dirs, files in os.walk(jena_dir):
        if 'sparql' in files:
            sparql_found = True
            break
    assert sparql_found, "Jena 'sparql' binary not found in /home/user/jena."

def test_deadlocks_json_exists():
    """Test that the output deadlocks.json exists."""
    json_path = '/home/user/deadlocks.json'
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist."

def test_deadlocks_json_content():
    """Test that deadlocks.json contains the correct deadlock pairs."""
    json_path = '/home/user/deadlocks.json'
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected JSON array, got {type(data).__name__}."

    expected_data = [
        {"tx1": "T1", "tx2": "T2"},
        {"tx1": "T5", "tx2": "T6"}
    ]

    # Sort both just in case, though the prompt requires the output to be sorted
    try:
        sorted_data = sorted(data, key=lambda x: x.get('tx1', ''))
    except TypeError:
        pytest.fail("Elements in JSON array are not dictionaries as expected.")

    assert sorted_data == expected_data, f"JSON content does not match expected deadlocks. Got: {sorted_data}"
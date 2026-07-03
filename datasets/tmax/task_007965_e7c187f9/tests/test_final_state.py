# test_final_state.py

import os
import json
import pytest

def test_analyze_script_exists_and_executable():
    """Test that the analyze.sh script exists and is executable."""
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Missing required file: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_result_json_exists():
    """Test that the result.json file exists."""
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Missing output file: {result_path}"

def test_result_json_content():
    """Test that the result.json file contains the correct central node and FOAF array."""
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Missing output file: {result_path}"

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON")

    assert "central_node" in data, "JSON missing 'central_node' key"
    assert "foaf" in data, "JSON missing 'foaf' key"

    assert data["central_node"] == "Alice", f"Incorrect central node: {data['central_node']}"

    expected_foaf = ["Charlie", "Eve", "Frank"]
    assert isinstance(data["foaf"], list), "'foaf' must be a JSON array"
    assert data["foaf"] == expected_foaf, f"Incorrect FOAF array: {data['foaf']} (expected {expected_foaf})"
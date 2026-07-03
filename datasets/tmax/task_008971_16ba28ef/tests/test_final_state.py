# test_final_state.py

import os
import json
import pytest

def test_script_exists():
    """Test that the python script was created."""
    script_path = "/home/user/parse_artifacts.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist. Did you create it?"

def test_json_output_exists():
    """Test that the curated_artifacts.json file was created."""
    json_path = "/home/user/curated_artifacts.json"
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist. Did you run your script?"

def test_json_output_content():
    """Test that the curated_artifacts.json file contains the correct parsed metadata."""
    json_path = "/home/user/curated_artifacts.json"
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    expected_data = {
        "001": {
            "type": "GCODE",
            "max_z": 12.4
        },
        "002": {
            "type": "ELF",
            "entry_point": "0x8048100"
        },
        "003": {
            "type": "GCODE",
            "max_z": 1.1
        }
    }

    assert isinstance(data, dict), f"Expected the JSON root to be a dictionary, got {type(data).__name__}"

    for key, expected_val in expected_data.items():
        assert key in data, f"Missing artifact ID '{key}' in JSON output."
        assert data[key] == expected_val, f"Incorrect data for artifact '{key}'. Expected {expected_val}, got {data[key]}"

    # Check for any extra keys
    extra_keys = set(data.keys()) - set(expected_data.keys())
    assert not extra_keys, f"Found unexpected artifact IDs in JSON output: {extra_keys}"
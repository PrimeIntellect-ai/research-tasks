# test_final_state.py

import os
import json
import pytest

def test_output_json_exists_and_correct():
    """Test that output.json exists and contains the correct data."""
    output_path = "/home/user/output.json"
    assert os.path.exists(output_path), f"File {output_path} does not exist."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_path} is not valid JSON.")

    assert "user_profiles" in data, "Key 'user_profiles' missing from output.json"
    assert "item_similarities" in data, "Key 'item_similarities' missing from output.json"

    expected_profiles = [
        {"user_id": "u1", "category": "A", "alpha": 2, "beta": 2},
        {"user_id": "u2", "category": "A", "alpha": 2, "beta": 1},
        {"user_id": "u2", "category": "B", "alpha": 2, "beta": 1},
        {"user_id": "u3", "category": "B", "alpha": 3, "beta": 1}
    ]

    expected_similarities = [
        {"item_1": "i1", "item_2": "i2", "jaccard": 0.3333},
        {"item_1": "i1", "item_2": "i3", "jaccard": 0.0},
        {"item_1": "i2", "item_2": "i3", "jaccard": 0.5}
    ]

    assert data["user_profiles"] == expected_profiles, "user_profiles do not match expected values or sorting."
    assert data["item_similarities"] == expected_similarities, "item_similarities do not match expected values or sorting."

def test_reproducibility_script_exists():
    """Test that the reproducibility bash script was created."""
    script_path = "/home/user/test_reproducibility.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

def test_repro_status_correct():
    """Test that repro_status.txt contains the correct output."""
    status_path = "/home/user/repro_status.txt"
    assert os.path.exists(status_path), f"File {status_path} does not exist."

    with open(status_path, "r") as f:
        content = f.read().strip()

    assert content == "REPRODUCIBLE", f"Expected 'REPRODUCIBLE' in {status_path}, got '{content}'"
# test_final_state.py

import os
import json
import math
import pytest

def test_result_file_exists():
    """Test that the result.json file was generated."""
    file_path = "/home/user/result.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you run the script?"

def test_result_content_correct():
    """Test that the result.json contains the correct final position."""
    file_path = "/home/user/result.json"
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    assert "final_position" in data, "Key 'final_position' is missing from result.json."

    expected_position = 1.25
    actual_position = data["final_position"]

    assert isinstance(actual_position, (int, float)), "final_position must be a number."
    assert math.isclose(actual_position, expected_position, rel_tol=1e-5, abs_tol=1e-5), \
        f"Expected final_position to be close to {expected_position}, but got {actual_position}."

def test_simulate_script_fixes():
    """Test that the simulate.py script has the required fixes."""
    file_path = "/home/user/simulation/simulate.py"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read()

    # Check that the off-by-one error is fixed
    assert "len(forces) - 1" not in content, "The off-by-one error (len(forces) - 1) is still present."

    # Check that the assertion is added
    assert "assert velocity >= 0.0" in content, "The required assertion 'assert velocity >= 0.0' is missing."
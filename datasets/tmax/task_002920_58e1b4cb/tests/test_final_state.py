# test_final_state.py
import os
import json
import math
import pytest

def test_tracker_cpp_exists():
    """Verify that the C++ source file exists."""
    assert os.path.isfile("/home/user/tracker.cpp"), "/home/user/tracker.cpp does not exist."

def test_tracker_executable_exists():
    """Verify that the compiled executable exists."""
    assert os.path.isfile("/home/user/tracker"), "/home/user/tracker executable does not exist."
    assert os.access("/home/user/tracker", os.X_OK), "/home/user/tracker is not executable."

def test_embeddings_log_json_exists_and_correct():
    """Verify that the embeddings_log.json file exists and contains correct normalized embeddings."""
    json_path = "/home/user/embeddings_log.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    expected = {
        "exp_001": [0.6000, 0.8000, 0.0000],
        "exp_002": [0.7071, 0.0000, 0.7071],
        "exp_003": [0.0000, 1.0000, 0.0000],
        "exp_004": [0.0000, 0.0000, 0.0000],
        "exp_005": [0.5774, -0.5774, 0.5774]
    }

    assert isinstance(data, dict), "The root of the JSON file must be an object/dictionary."
    assert set(data.keys()) == set(expected.keys()), f"Expected keys {set(expected.keys())}, but got {set(data.keys())}."

    for k, v in expected.items():
        assert isinstance(data[k], list), f"Value for {k} must be a list."
        assert len(data[k]) == 3, f"Value for {k} must have exactly 3 elements."
        for i, (a, b) in enumerate(zip(data[k], v)):
            assert isinstance(a, (int, float)), f"Element {i} of {k} must be a number."
            assert math.isclose(a, b, abs_tol=1e-3), f"Mismatch in {k} at index {i}: expected {b}, got {a}."
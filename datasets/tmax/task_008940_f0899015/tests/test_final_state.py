# test_final_state.py

import os
import json
import pstats
import pytest

def test_optimize_script_exists():
    """Check if the optimize.py script exists."""
    file_path = "/home/user/optimize.py"
    assert os.path.isfile(file_path), f"Script not found: {file_path}"

def test_profile_out_exists_and_valid():
    """Check if profile.out exists and is a valid cProfile dump."""
    file_path = "/home/user/profile.out"
    assert os.path.isfile(file_path), f"Profile output not found: {file_path}"

    try:
        stats = pstats.Stats(file_path)
        assert stats.total_calls > 0 or len(stats.stats) > 0, "Profile stats are empty."
    except Exception as e:
        pytest.fail(f"Failed to load profile.out as a valid pstats file: {e}")

def test_final_state_json_exists_and_correct():
    """Check if final_state.json exists and contains the correct rounded values."""
    file_path = "/home/user/final_state.json"
    assert os.path.isfile(file_path), f"Output file not found: {file_path}"

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse final_state.json: {e}")

    assert "y0" in data, "Key 'y0' missing in final_state.json"
    assert "y1" in data, "Key 'y1' missing in final_state.json"

    # The expected values are 0.00200
    expected_val = 0.00200

    assert abs(data["y0"] - expected_val) < 1e-5, f"Expected y0 to be close to {expected_val}, got {data['y0']}"
    assert abs(data["y1"] - expected_val) < 1e-5, f"Expected y1 to be close to {expected_val}, got {data['y1']}"
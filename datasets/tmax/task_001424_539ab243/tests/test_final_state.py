# test_final_state.py

import json
import os
import pytest

def test_summary_json_exists_and_valid():
    """Test that summary.json exists, contains the correct keys, and values have expected types/bounds."""
    file_path = "/home/user/summary.json"
    assert os.path.exists(file_path), f"Missing file: {file_path} does not exist."

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert "avg_posterior_class1" in data, "Missing key 'avg_posterior_class1' in summary.json."
    assert "best_c_mode" in data, "Missing key 'best_c_mode' in summary.json."

    avg_post = data["avg_posterior_class1"]
    best_c = data["best_c_mode"]

    assert isinstance(avg_post, (int, float)), "'avg_posterior_class1' must be a number."
    assert 0.0 <= avg_post <= 1.0, "'avg_posterior_class1' must be a probability between 0 and 1."

    assert isinstance(best_c, (int, float)), "'best_c_mode' must be a number."
    assert best_c in [0.01, 0.1, 1.0, 10.0], f"'best_c_mode' must be one of the grid values [0.01, 0.1, 1.0, 10.0], got {best_c}."
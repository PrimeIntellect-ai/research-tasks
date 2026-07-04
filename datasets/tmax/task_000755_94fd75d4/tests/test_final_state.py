# test_final_state.py

import os
import json
import pytest

def test_posterior_stats_file_exists():
    """Check if the posterior_stats.json file exists."""
    assert os.path.exists("/home/user/posterior_stats.json"), "The file /home/user/posterior_stats.json does not exist."

def test_posterior_stats_content():
    """Check if the posterior_stats.json file contains the correct keys and values."""
    file_path = "/home/user/posterior_stats.json"
    assert os.path.exists(file_path), "The file /home/user/posterior_stats.json does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {file_path} is not a valid JSON file.")

    assert "mean" in data, "The key 'mean' is missing from the JSON file."
    assert "std" in data, "The key 'std' is missing from the JSON file."

    mean = data["mean"]
    std = data["std"]

    assert isinstance(mean, (int, float)), f"Expected 'mean' to be a number, got {type(mean)}."
    assert isinstance(std, (int, float)), f"Expected 'std' to be a number, got {type(std)}."

    assert 2.40 <= mean <= 2.55, f"The calculated mean ({mean}) is not within the expected range [2.40, 2.55]."
    assert 0.20 <= std <= 0.25, f"The calculated std ({std}) is not within the expected range [0.20, 0.25]."
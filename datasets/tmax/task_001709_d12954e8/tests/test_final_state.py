# test_final_state.py

import os
import json
import pytest

def test_posterior_json_exists():
    """Verify that the posterior.json file exists."""
    path = "/home/user/posterior.json"
    assert os.path.isfile(path), f"Expected file {path} to exist."

def test_posterior_json_format_and_values():
    """Verify the contents of posterior.json."""
    path = "/home/user/posterior.json"
    assert os.path.isfile(path), f"Expected file {path} to exist before checking contents."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert "mean_theta" in data, "JSON is missing the 'mean_theta' key."
    assert "acceptance_rate" in data, "JSON is missing the 'acceptance_rate' key."

    mean_theta = data["mean_theta"]
    acceptance_rate = data["acceptance_rate"]

    assert isinstance(mean_theta, (int, float)), "'mean_theta' must be a number."
    assert isinstance(acceptance_rate, (int, float)), "'acceptance_rate' must be a number."

    assert 0.45 <= mean_theta <= 0.55, f"Expected 'mean_theta' to be between 0.45 and 0.55, but got {mean_theta}."
    assert 0.15 <= acceptance_rate <= 0.50, f"Expected 'acceptance_rate' to be between 0.15 and 0.50, but got {acceptance_rate}."
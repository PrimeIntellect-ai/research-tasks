# test_final_state.py

import os
import json
import pytest

def test_venv_exists():
    """Test that the virtual environment was created."""
    venv_python = "/home/user/bio_env/bin/python"
    assert os.path.exists(venv_python), f"Virtual environment Python executable not found at {venv_python}"

def test_results_json_exists():
    """Test that the results.json file exists."""
    results_file = "/home/user/results.json"
    assert os.path.isfile(results_file), f"File {results_file} does not exist."

def test_results_json_content():
    """Test the structure and content of the results.json file."""
    results_file = "/home/user/results.json"
    with open(results_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} does not contain valid JSON.")

    # Check required keys
    assert "optimal_weights" in data, "Missing 'optimal_weights' key in results.json."
    assert "seq_train_power" in data, "Missing 'seq_train_power' key in results.json."
    assert "ranking" in data, "Missing 'ranking' key in results.json."

    # Validate optimal_weights
    weights = data["optimal_weights"]
    assert isinstance(weights, dict), "'optimal_weights' should be a dictionary."
    for base in ["A", "C", "G", "T"]:
        assert base in weights, f"Missing base '{base}' in 'optimal_weights'."
        assert isinstance(weights[base], (int, float)), f"Weight for '{base}' must be a number."

    # Validate seq_train_power
    power = data["seq_train_power"]
    assert isinstance(power, (int, float)), "'seq_train_power' must be a number."
    assert power > 0.1, f"'seq_train_power' is expected to be > 0.1, got {power}."

    # Validate ranking
    ranking = data["ranking"]
    assert isinstance(ranking, list), "'ranking' should be a list."
    assert len(ranking) == 4, f"'ranking' should contain exactly 4 elements, got {len(ranking)}."

    top_two = set(ranking[:2])
    assert top_two == {"seq_train", "seq_C"}, f"Top two sequences must be 'seq_train' and 'seq_C', got {ranking[:2]}."
    assert ranking[2] == "seq_A", f"The third sequence must be 'seq_A', got '{ranking[2]}'."
    assert ranking[3] == "seq_B", f"The fourth sequence must be 'seq_B', got '{ranking[3]}'."
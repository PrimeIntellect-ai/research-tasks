# test_final_state.py

import os
import json
import pytest

def test_experiment_summary_exists():
    """Test that the experiment_summary.json file exists."""
    file_path = '/home/user/experiment_summary.json'
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_experiment_summary_contents():
    """Test that the experiment_summary.json file contains the correct values."""
    file_path = '/home/user/experiment_summary.json'

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_keys = {"best_num_layers", "best_hidden_size", "p_value", "inference_sum"}
    actual_keys = set(data.keys())

    assert expected_keys.issubset(actual_keys), f"Missing keys in JSON. Expected {expected_keys}, got {actual_keys}."

    assert data["best_num_layers"] == 3, f"Expected best_num_layers to be 3, got {data['best_num_layers']}."
    assert data["best_hidden_size"] == 128, f"Expected best_hidden_size to be 128, got {data['best_hidden_size']}."

    # Check p-value rounded to 4 decimal places
    assert isinstance(data["p_value"], (int, float)), "p_value must be a float."
    assert round(data["p_value"], 4) == 0.0019, f"Expected p_value to be 0.0019, got {data['p_value']}."

    # Check inference_sum rounded to 4 decimal places
    assert isinstance(data["inference_sum"], (int, float)), "inference_sum must be a float."
    assert round(data["inference_sum"], 4) == 0.3277, f"Expected inference_sum to be 0.3277, got {data['inference_sum']}."
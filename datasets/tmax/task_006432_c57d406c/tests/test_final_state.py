# test_final_state.py

import os
import json
import pytest

JSON_PATH = "/home/user/analysis.json"
PLOT_PATH = "/home/user/distance_distribution.png"

def test_json_file_exists():
    """Check if the analysis.json file was created."""
    assert os.path.exists(JSON_PATH), f"Error: {JSON_PATH} not found. Did you save the JSON file?"
    assert os.path.isfile(JSON_PATH), f"Error: {JSON_PATH} is not a valid file."

def test_plot_file_exists():
    """Check if the distance_distribution.png file was created."""
    assert os.path.exists(PLOT_PATH), f"Error: {PLOT_PATH} not found. Did you save the plot?"
    assert os.path.isfile(PLOT_PATH), f"Error: {PLOT_PATH} is not a valid file."
    assert os.path.getsize(PLOT_PATH) > 0, f"Error: {PLOT_PATH} is empty."

def test_json_contents():
    """Validate the contents of the analysis.json file."""
    assert os.path.exists(JSON_PATH), f"Cannot test contents, {JSON_PATH} is missing."

    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Error: {JSON_PATH} does not contain valid JSON.")

    required_keys = [
        "sequence_length", 
        "mc_mean_squared_distance", 
        "analytical_mean_squared_distance", 
        "relative_error"
    ]

    for key in required_keys:
        assert key in data, f"Error: Missing key '{key}' in {JSON_PATH}."

    # Validate sequence length
    assert data["sequence_length"] == 110, \
        f"Error: Incorrect sequence_length. Expected 110, got {data['sequence_length']}."

    # Validate analytical distance
    assert data["analytical_mean_squared_distance"] == 109, \
        f"Error: Incorrect analytical_mean_squared_distance. Expected 109, got {data['analytical_mean_squared_distance']}."

    # Validate MC distance (statistical range check)
    mc_dist = data["mc_mean_squared_distance"]
    assert isinstance(mc_dist, (int, float)), "Error: mc_mean_squared_distance must be a number."
    assert 95 <= mc_dist <= 125, \
        f"Error: mc_mean_squared_distance {mc_dist} is outside the expected statistical range [95, 125] for 10,000 iterations."

    # Validate relative error
    expected_error = abs(mc_dist - 109) / 109.0
    reported_error = data["relative_error"]
    assert isinstance(reported_error, (int, float)), "Error: relative_error must be a number."
    assert abs(expected_error - reported_error) <= 1e-4, \
        f"Error: relative_error calculation is incorrect. Expected approx {expected_error}, got {reported_error}."
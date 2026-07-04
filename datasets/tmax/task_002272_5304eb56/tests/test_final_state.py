# test_final_state.py

import os
import json
import math
import pytest

JSON_PATH = '/home/user/training_entry.json'
PLOT_PATH = '/home/user/kinetics_plot.png'

def test_files_exist():
    assert os.path.exists(JSON_PATH), f"The output JSON file {JSON_PATH} is missing."
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} must be a file."

    assert os.path.exists(PLOT_PATH), f"The plot file {PLOT_PATH} is missing."
    assert os.path.isfile(PLOT_PATH), f"{PLOT_PATH} must be a file."

def test_json_structure_and_graph_features():
    assert os.path.exists(JSON_PATH), f"Cannot test JSON structure because {JSON_PATH} is missing."
    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{JSON_PATH} is not a valid JSON file.")

    assert "graph_features" in data, "Key 'graph_features' missing from JSON."
    gf = data["graph_features"]

    expected_gf = {
        "A": {"in": 0, "out": 1},
        "B": {"in": 1, "out": 1},
        "C": {"in": 1, "out": 0}
    }

    assert gf == expected_gf, f"Graph features are incorrect. Expected {expected_gf}, got {gf}."

def test_json_max_b():
    assert os.path.exists(JSON_PATH), f"Cannot test max_B_simulated because {JSON_PATH} is missing."
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)

    assert "max_B_simulated" in data, "Key 'max_B_simulated' missing from JSON."
    max_b = data["max_B_simulated"]

    assert isinstance(max_b, (int, float)), f"'max_B_simulated' must be a number, got {type(max_b)}."

    expected_max_b = 46.5457
    assert math.isclose(max_b, expected_max_b, abs_tol=0.2), \
        f"'max_B_simulated' is incorrect. Expected around {expected_max_b}, got {max_b}."

def test_json_mses():
    assert os.path.exists(JSON_PATH), f"Cannot test MSE values because {JSON_PATH} is missing."
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)

    for key in ["mse_A", "mse_B", "mse_C"]:
        assert key in data, f"Key '{key}' missing from JSON."
        assert isinstance(data[key], (int, float)), f"'{key}' must be a number."

    expected_mses = {
        "mse_A": 3.864,
        "mse_B": 3.829,
        "mse_C": 3.511
    }

    for key, expected_val in expected_mses.items():
        actual_val = data[key]
        assert math.isclose(actual_val, expected_val, abs_tol=0.5), \
            f"'{key}' is incorrect. Expected around {expected_val}, got {actual_val}."
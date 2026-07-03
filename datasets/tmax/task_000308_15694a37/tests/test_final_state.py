# test_final_state.py

import os
import json
import pytest

def test_obs_data_h5_exists():
    path = "/home/user/obs_data.h5"
    assert os.path.exists(path), f"HDF5 file not found at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_optimize_script_exists():
    path = "/home/user/optimize.py"
    assert os.path.exists(path), f"Optimization script not found at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_best_params_json_exists():
    path = "/home/user/best_params.json"
    assert os.path.exists(path), f"Output file not found at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_best_params_structure_and_metric():
    path = "/home/user/best_params.json"
    assert os.path.exists(path), f"Output file not found at {path}"

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {path} is not valid JSON")

    required_keys = {"p1", "p2", "p3", "energy"}
    missing_keys = required_keys - set(data.keys())
    assert not missing_keys, f"JSON is missing required keys: {missing_keys}"

    energy = data["energy"]
    assert isinstance(energy, (int, float)), f"Energy must be a number, got {type(energy)}"

    threshold = 5.0
    assert energy <= threshold, f"Metric threshold failed: energy value {energy} is not <= {threshold}"
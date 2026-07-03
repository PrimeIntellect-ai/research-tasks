# test_final_state.py

import os
import json
import pytest

def test_map_estimates_file():
    json_path = "/home/user/map_estimates.json"
    assert os.path.isfile(json_path), f"Expected JSON file at {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "k" in data, "Key 'k' is missing from the JSON file."
    assert "c" in data, "Key 'c' is missing from the JSON file."

    k_val = data["k"]
    c_val = data["c"]

    assert isinstance(k_val, (int, float)), "'k' value must be a number."
    assert isinstance(c_val, (int, float)), "'c' value must be a number."

    assert 4.5 <= k_val <= 5.5, f"Estimated 'k' ({k_val}) is outside the acceptable range [4.5, 5.5]."
    assert 0.3 <= c_val <= 0.7, f"Estimated 'c' ({c_val}) is outside the acceptable range [0.3, 0.7]."

def test_script_modifications():
    script_path = "/home/user/fit_model.py"
    assert os.path.isfile(script_path), f"Script file {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    # Check for multiprocessing pool
    assert "pool=" in content or "Pool(" in content, "The script does not appear to use multiprocessing.Pool in the sampler."
    assert "emcee.EnsembleSampler" in content, "The script is missing emcee.EnsembleSampler."
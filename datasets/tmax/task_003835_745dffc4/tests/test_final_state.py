# test_final_state.py

import os
import json
import pytest

def test_simulate_py_fixed():
    """Check that /home/user/simulate.py has been modified to fix the bug."""
    file_path = "/home/user/simulate.py"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    assert "def simulate_v1" in content, "simulate_v1 function is missing."
    assert "def simulate_v2" in content, "simulate_v2 function is missing."
    assert "scale=1.05" not in content, "The bug (scale=1.05) in simulate_v2 was not fixed."

def test_compare_py_exists():
    """Check that /home/user/compare.py exists."""
    file_path = "/home/user/compare.py"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_comparison_json():
    """Check that /home/user/comparison.json exists, is valid JSON, and has correct values."""
    json_path = "/home/user/comparison.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "wasserstein_distance" in data, "Key 'wasserstein_distance' missing from JSON."
    assert "ks_pvalue" in data, "Key 'ks_pvalue' missing from JSON."

    wasserstein_distance = data["wasserstein_distance"]
    ks_pvalue = data["ks_pvalue"]

    assert isinstance(wasserstein_distance, (int, float)), "wasserstein_distance must be a float."
    assert isinstance(ks_pvalue, (int, float)), "ks_pvalue must be a float."

    assert wasserstein_distance < 0.5, f"Wasserstein distance {wasserstein_distance} is too high, bug likely not fixed properly."
    assert ks_pvalue > 0.01, f"KS p-value {ks_pvalue} is too low, distributions do not match."
# test_final_state.py

import os
import json
import pytest
import numpy as np

def test_analysis_output_exists():
    path = "/home/user/analysis_output.json"
    assert os.path.isfile(path), f"Analysis output missing: {path}"

def test_analysis_output_structure():
    path = "/home/user/analysis_output.json"
    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {path}")

    expected_keys = {"k_mean", "k_ci_lower", "k_ci_upper", "fitted_areas"}
    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"Missing keys in analysis output: {missing_keys}"

    assert isinstance(data["fitted_areas"], list), "fitted_areas must be a list"
    assert len(data["fitted_areas"]) == 1000, f"Expected 1000 fitted_areas, got {len(data['fitted_areas'])}"

def test_fitted_areas_mse():
    path = "/home/user/analysis_output.json"
    with open(path, 'r') as f:
        data = json.load(f)

    times = np.linspace(0, 100, 1000)
    true_areas = 12.5 * np.exp(-0.045 * times) + 1.2

    agent_areas = np.array(data['fitted_areas'])
    mse = np.mean((agent_areas - true_areas)**2)

    assert mse <= 0.01, f"MSE of fitted_areas is too high: {mse} > 0.01"

def test_c_library_built():
    path = "/app/specfit-2.1.0/libspecfit.so"
    assert os.path.isfile(path), f"Compiled shared library missing: {path}"
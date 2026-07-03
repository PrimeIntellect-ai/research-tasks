# test_final_state.py

import os
import sys
import json
import numpy as np
import pandas as pd
import pytest

def test_solution_json_exists_and_valid():
    solution_path = '/home/user/solution.json'
    assert os.path.isfile(solution_path), f"Missing solution file: {solution_path}"

    with open(solution_path, 'r') as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {solution_path} is not a valid JSON.")

    expected_keys = {"A1", "mu1", "sigma1", "A2", "mu2", "sigma2"}
    assert set(params.keys()) == expected_keys, f"JSON must contain exactly these keys: {expected_keys}"

    for k in expected_keys:
        assert isinstance(params[k], (int, float)), f"Parameter {k} must be a number."

def test_spectrosim_importable():
    sys.path.append('/app/spectrosim')
    try:
        import spectrosim
    except ImportError as e:
        pytest.fail(f"Failed to import spectrosim. Did you fix the Makefile and compile the package? Error: {e}")

def test_mse_metric():
    solution_path = '/home/user/solution.json'
    data_path = '/home/user/data/spectrum.csv'

    assert os.path.isfile(solution_path), f"Missing solution file: {solution_path}"
    assert os.path.isfile(data_path), f"Missing data file: {data_path}"

    with open(solution_path, 'r') as f:
        params = json.load(f)

    df = pd.read_csv(data_path)
    x = df['wavelength'].values
    y_true = df['intensity'].values

    sys.path.append('/app/spectrosim')
    import spectrosim

    y_sim = spectrosim.simulate(
        x,
        params['A1'], params['mu1'], params['sigma1'],
        params['A2'], params['mu2'], params['sigma2']
    )

    mse = np.mean((y_true - y_sim)**2)
    threshold = 1e-4

    assert mse <= threshold, f"MSE is {mse}, which is greater than the threshold {threshold}."
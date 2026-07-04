# test_final_state.py
import json
import os
import requests
import numpy as np
import pandas as pd
import pytest

def test_best_params_exists_and_valid():
    params_file = "/home/user/best_params.json"
    assert os.path.isfile(params_file), f"Output file {params_file} is missing."

    with open(params_file, 'r') as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {params_file} is not valid JSON.")

    for key in ["k1", "k2", "k3"]:
        assert key in params, f"Key '{key}' missing from {params_file}."
        assert isinstance(params[key], (int, float)), f"Value for '{key}' must be a number."

def test_simulation_mse():
    params_file = "/home/user/best_params.json"
    assert os.path.isfile(params_file), f"Output file {params_file} is missing."

    with open(params_file, 'r') as f:
        params = json.load(f)

    try:
        resp = requests.post("http://127.0.0.1:8000/simulate", json=params, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to communicate with the API server at http://127.0.0.1:8000/simulate. Ensure services are running and the bug in the C++ worker is fixed. Error: {e}")

    sim_data = resp.json()
    assert 't' in sim_data, "Simulation response missing 't' array."
    assert 'P' in sim_data, "Simulation response missing 'P' array."

    obs_file = "/app/data/observed.csv"
    assert os.path.isfile(obs_file), f"Observed data file {obs_file} is missing."

    obs_df = pd.read_csv(obs_file)
    assert 't' in obs_df.columns and 'P' in obs_df.columns, "Observed data missing 't' or 'P' columns."

    sim_t = np.array(sim_data['t'])
    sim_P = np.array(sim_data['P'])

    # Interpolate simulation to observed timepoints
    sim_P_interp = np.interp(obs_df['t'].values, sim_t, sim_P)

    mse = np.mean((sim_P_interp - obs_df['P'].values)**2)
    threshold = 0.01

    assert mse <= threshold, f"MSE {mse:.6f} is greater than the threshold {threshold}. Parameters used: {params}"
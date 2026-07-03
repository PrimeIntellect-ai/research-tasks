# test_final_state.py
import os
import numpy as np
import pandas as pd

def exact_B(k1, k2, t):
    if np.isclose(k1, k2):
        return k1 * t * np.exp(-k1 * t)
    return (k1 / (k2 - k1)) * (np.exp(-k1 * t) - np.exp(-k2 * t))

def test_fitted_params_mse():
    params_file = '/home/user/fitted_params.csv'
    assert os.path.exists(params_file), f"Error: {params_file} not found."

    with open(params_file, 'r') as f:
        line = f.read().strip()

    parts = line.split(',')
    assert len(parts) == 2, f"Expected exactly two comma-separated values in {params_file}, but got: {line}"

    try:
        k1, k2 = float(parts[0]), float(parts[1])
    except ValueError:
        assert False, f"Could not parse k1 and k2 as floats from: {line}"

    data_file = '/home/user/data/spectroscopy.csv'
    assert os.path.exists(data_file), f"Data file {data_file} is missing."

    data = pd.read_csv(data_file)
    assert 'time' in data.columns and 'signal' in data.columns, "Data file must contain 'time' and 'signal' columns."

    t_data = data['time'].values
    signal_data = data['signal'].values

    predicted_signal = exact_B(k1, k2, t_data)
    mse = np.mean((predicted_signal - signal_data)**2)

    threshold = 0.005
    assert mse < threshold, f"MSE is {mse:.6f}, which is not less than the threshold {threshold}. Fitted parameters: k1={k1}, k2={k2}"
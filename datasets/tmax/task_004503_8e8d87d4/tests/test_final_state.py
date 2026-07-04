# test_final_state.py
import os
import numpy as np
import pandas as pd
import pytest

def test_pde_result_accuracy():
    """
    Validates that the numerical PDE solution is saved correctly and meets the accuracy threshold.
    """
    result_path = "/home/user/pde_result.csv"

    # Check if file exists
    assert os.path.isfile(result_path), f"Expected result file not found at {result_path}"

    # Load the CSV
    try:
        df = pd.read_csv(result_path)
    except Exception as e:
        pytest.fail(f"Failed to read {result_path} as a CSV: {e}")

    # Check columns
    assert 'x' in df.columns, "CSV must contain an 'x' column"
    assert 'u' in df.columns, "CSV must contain a 'u' column"

    x = df['x'].values
    u_agent = df['u'].values

    # Check number of points
    assert len(x) == 101, f"Expected exactly 101 points, but got {len(x)}"

    # Check domain bounds
    assert np.isclose(x[0], 0.0), f"First x value should be 0.0, got {x[0]}"
    assert np.isclose(x[-1], 10.0), f"Last x value should be 10.0, got {x[-1]}"

    # Calculate expected analytical solution
    # Parameters from the audio: alpha = 0.05, L = 10.0, T = 20.0
    alpha = 0.05
    L = 10.0
    T = 20.0

    u_true = np.sin(np.pi * x / L) * np.exp(-alpha * (np.pi / L)**2 * T)

    # Calculate maximum absolute error
    max_error = np.max(np.abs(u_agent - u_true))
    threshold = 0.005

    assert max_error <= threshold, (
        f"Maximum absolute error is too high. "
        f"Got max_error = {max_error:.6f}, which is greater than the threshold of {threshold}."
    )
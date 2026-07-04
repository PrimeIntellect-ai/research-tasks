# test_final_state.py
import os
import numpy as np
import pandas as pd

def test_trajectory_mse():
    """Verify that the generated trajectory has an MSE <= 0.01 compared to the analytical solution."""
    csv_path = '/home/user/trajectory.csv'
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        assert False, f"Failed to read {csv_path} as a CSV: {e}"

    assert 't' in df.columns, "CSV must contain a 't' column."
    assert 'y' in df.columns, "CSV must contain a 'y' column."

    t = df['t'].values
    y_agent = df['y'].values

    assert len(t) == 100, f"Expected exactly 100 points in the trajectory, but got {len(t)}."

    # Verify the time span
    assert np.isclose(t[0], 0.0), f"Expected start time t=0.0, got t={t[0]}"
    assert np.isclose(t[-1], 10.0), f"Expected end time t=10.0, got t={t[-1]}"

    # Analytical solution: dy/dt = -0.5 * y, Y0 = 42
    Y0 = 42.0
    y_true = Y0 * np.exp(-0.5 * t)

    mse = np.mean((y_agent - y_true)**2)

    assert mse <= 0.01, f"MSE is {mse}, which is above the maximum allowed threshold of 0.01."
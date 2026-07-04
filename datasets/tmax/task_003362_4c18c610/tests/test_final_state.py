# test_final_state.py

import os
import numpy as np
import pytest

def test_trajectory_mse():
    file_path = '/home/user/trajectory.tsv'
    assert os.path.isfile(file_path), f"Missing trajectory file at {file_path}"

    try:
        data = np.loadtxt(file_path, skiprows=1)
    except Exception as e:
        pytest.fail(f"Failed to load {file_path} with numpy: {e}")

    assert data.shape[1] >= 2, f"Expected at least 2 columns in {file_path}, but got {data.shape[1]}"

    t = data[:, 0]
    y_agent = data[:, 1]

    # Expected analytical solution
    f_expected = 2.5
    omega = 2 * np.pi * f_expected
    y_true = np.cos(omega * t)

    mse = np.mean((y_agent - y_true)**2)

    assert mse <= 0.05, f"MSE between agent trajectory and analytical solution is {mse}, which is > threshold 0.05"
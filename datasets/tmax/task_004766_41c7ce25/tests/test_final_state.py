# test_final_state.py

import os
import math
import pytest

def test_training_data_exists_and_valid():
    h5_path = "/home/user/training_data.h5"
    assert os.path.isfile(h5_path), f"File {h5_path} does not exist."

    # Check HDF5 magic number to ensure it's a valid HDF5 file
    with open(h5_path, 'rb') as f:
        magic = f.read(8)
        assert magic == b'\x89HDF\r\n\x1a\n', f"File {h5_path} is not a valid HDF5 file."

    # Attempt to use h5py to validate the contents if available
    try:
        import h5py
        import numpy as np
    except ImportError:
        pytest.skip("h5py or numpy not installed, skipping content validation")

    with h5py.File(h5_path, 'r') as f:
        assert 'simulated_trajectories' in f, "Dataset 'simulated_trajectories' not found in HDF5 file."
        data = f['simulated_trajectories'][:]

        assert data.shape == (1000, 5), f"Expected shape (1000, 5), got {data.shape}"

        expected_y0 = [550.0, 2200.0, 330.0, 440.0, 660.0]
        np.testing.assert_allclose(data[0], expected_y0, atol=1e-5, err_msg="Initial conditions do not match expected values.")

        expected_final = [346.903, 563.856, 318.000, 332.449, 361.353]
        np.testing.assert_allclose(data[-1], expected_final, atol=1e-2, err_msg="Final row values do not match expected values.")

def test_stability_plot_exists():
    plot_path = "/home/user/stability_plot.png"
    assert os.path.isfile(plot_path), f"File {plot_path} does not exist."

    # Check PNG magic number
    with open(plot_path, 'rb') as f:
        magic = f.read(8)
        assert magic == b'\x89PNG\r\n\x1a\n', f"File {plot_path} is not a valid PNG file."
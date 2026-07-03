# test_final_state.py

import os
import h5py
import numpy as np
import pytest

H5_PATH = '/home/user/model_results.h5'
CLEAN_SIGNAL_PATH = '/app/s_clean.npy'

def test_model_results_h5_exists():
    """Check if the final HDF5 file exists at the required path."""
    assert os.path.exists(H5_PATH), f"The output file {H5_PATH} does not exist."

def test_model_results_datasets():
    """Ensure all required datasets are present in the root group of the HDF5 file."""
    expected_keys = [
        '/f1', '/f2', '/A1', '/A2', '/alpha1', '/alpha2',
        '/f1_std', '/f2_std', '/F_stat'
    ]
    with h5py.File(H5_PATH, 'r') as f:
        for k in expected_keys:
            assert k in f, f"Dataset {k} is missing from the HDF5 file."

def test_reconstruction_mse():
    """
    Reconstruct the signal using the agent's parameters, normalize it, 
    and verify that the Mean Squared Error against the ground truth is < 0.05.
    """
    with h5py.File(H5_PATH, 'r') as f:
        try:
            A1 = float(np.array(f['/A1']).item())
            A2 = float(np.array(f['/A2']).item())
            alpha1 = float(np.array(f['/alpha1']).item())
            alpha2 = float(np.array(f['/alpha2']).item())
            f1 = float(np.array(f['/f1']).item())
            f2 = float(np.array(f['/f2']).item())
        except Exception as e:
            pytest.fail(f"Failed to extract scalar parameters from HDF5: {e}")

    fs = 8000
    t = np.arange(fs) / fs

    # Reconstruct the 2-component damped oscillator signal
    agent_recon = A1 * np.exp(-alpha1 * t) * np.sin(2 * np.pi * f1 * t) + \
                  A2 * np.exp(-alpha2 * t) * np.sin(2 * np.pi * f2 * t)

    # Scale down by the factor used during WAV generation
    scale_factor = 32767.0 / 2.0
    agent_recon = agent_recon / scale_factor

    assert os.path.exists(CLEAN_SIGNAL_PATH), f"Ground truth file {CLEAN_SIGNAL_PATH} missing."
    s_clean = np.load(CLEAN_SIGNAL_PATH)

    mse = np.mean((s_clean - agent_recon)**2)

    threshold = 0.05
    assert mse < threshold, f"MSE of reconstructed signal is {mse:.5f}, which is not < {threshold}"
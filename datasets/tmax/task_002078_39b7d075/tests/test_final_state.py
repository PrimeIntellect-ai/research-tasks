# test_final_state.py

import os
import numpy as np
import pytest

def test_predictions_file_exists():
    assert os.path.isfile('/home/user/predictions.txt'), "/home/user/predictions.txt is missing. Did you generate the output file?"

def test_predictions_mse():
    predictions_path = '/home/user/predictions.txt'
    reference_path = '/tmp/reference_outputs.txt'

    assert os.path.isfile(predictions_path), f"File {predictions_path} not found."
    assert os.path.isfile(reference_path), f"Reference file {reference_path} not found."

    try:
        agent_outputs = np.loadtxt(predictions_path)
    except Exception as e:
        pytest.fail(f"Failed to load predictions from {predictions_path}. Ensure it contains one float per line. Error: {e}")

    try:
        reference_outputs = np.loadtxt(reference_path)
    except Exception as e:
        pytest.fail(f"Failed to load reference outputs. Error: {e}")

    assert agent_outputs.shape == reference_outputs.shape, \
        f"Predictions shape {agent_outputs.shape} does not match reference shape {reference_outputs.shape}. Expected exactly 10,000 lines."

    assert agent_outputs.size == 10000, \
        f"Expected exactly 10,000 predictions, but found {agent_outputs.size}."

    mse = np.mean((agent_outputs - reference_outputs)**2)

    assert mse < 1e-7, f"MSE {mse} is >= 1e-7. The predictions are not accurate enough compared to the oracle."
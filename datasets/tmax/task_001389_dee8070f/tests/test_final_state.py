# test_final_state.py

import os
import numpy as np
from scipy.io import wavfile
import pytest

def test_final_output_mse():
    agent_file = "/home/user/final_output.wav"
    reference_file = "/tmp/reference_output.wav"

    assert os.path.isfile(agent_file), f"Agent output file is missing: {agent_file}"
    assert os.path.isfile(reference_file), f"Reference output file is missing: {reference_file}"

    try:
        sr1, data1 = wavfile.read(agent_file)
    except Exception as e:
        pytest.fail(f"Failed to read agent's audio file {agent_file}: {e}")

    try:
        sr2, data2 = wavfile.read(reference_file)
    except Exception as e:
        pytest.fail(f"Failed to read reference audio file {reference_file}: {e}")

    assert sr1 == sr2, f"Sample rate mismatch: agent={sr1}, reference={sr2}"
    assert len(data1) == len(data2), f"Length mismatch: agent={len(data1)} samples, reference={len(data2)} samples"

    data1 = data1.astype(np.float32)
    data2 = data2.astype(np.float32)
    mse = np.mean((data1 - data2)**2)

    threshold = 0.001
    assert mse <= threshold, f"MSE is too high: {mse} (threshold is {threshold})"
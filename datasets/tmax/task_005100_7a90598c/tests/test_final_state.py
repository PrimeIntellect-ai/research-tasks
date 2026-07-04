# test_final_state.py

import json
import os
import numpy as np
import pytest

def test_spectrum_json_exists():
    path = '/home/user/spectrum.json'
    assert os.path.isfile(path), f"File {path} does not exist. The analyzer should output the PSD here."

def test_spectrum_mse():
    path = '/home/user/spectrum.json'
    assert os.path.isfile(path), f"File {path} missing."

    with open(path, 'r') as f:
        try:
            agent_psd = np.array(json.load(f), dtype=float)
        except Exception as e:
            pytest.fail(f"Could not load {path} as a JSON array of floats: {e}")

    N = 256
    assert len(agent_psd) == N, f"Expected {N} elements in PSD array, but got {len(agent_psd)}."

    exact_psd = np.zeros(N)
    # sin(x) -> complex amps at k=1 and k=255 are 0.5i and -0.5i
    # Initial PSD for k=1 and k=255 is 0.25
    # Decays by (e^{-0.1})^2 = e^{-0.2}
    exact_psd[1] = 0.25 * np.exp(-0.2)
    exact_psd[-1] = 0.25 * np.exp(-0.2)

    # 0.5*sin(3x) -> complex amps at k=3 and k=253 are 0.25i and -0.25i
    # Initial PSD for k=3 and k=253 is 0.0625
    # Decays by (e^{-0.9})^2 = e^{-1.8}
    exact_psd[3] = 0.0625 * np.exp(-1.8)
    exact_psd[-3] = 0.0625 * np.exp(-1.8)

    mse = np.mean((agent_psd - exact_psd)**2)
    threshold = 1e-4

    assert mse < threshold, f"MSE {mse} is not below the threshold {threshold}. The computed PSD does not match the theoretical expected PSD."

def test_final_state_json_exists():
    path = '/home/user/final_state.json'
    assert os.path.isfile(path), f"File {path} does not exist. The simulator should output the final spatial array here."
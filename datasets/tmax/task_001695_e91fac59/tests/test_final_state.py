# test_final_state.py
import os
import numpy as np
import pytest

def test_output_exists():
    assert os.path.isfile('/home/user/output.npy'), "The output file /home/user/output.npy was not generated."

def test_output_metric():
    agent_out_path = '/home/user/output.npy'
    ref_out_path = '/tmp/reference_output.npy'

    assert os.path.isfile(agent_out_path), f"Agent output missing at {agent_out_path}"
    assert os.path.isfile(ref_out_path), f"Reference output missing at {ref_out_path}"

    agent_out = np.load(agent_out_path)
    reference_out = np.load(ref_out_path)

    assert agent_out.shape == reference_out.shape, f"Shape mismatch: agent {agent_out.shape} vs ref {reference_out.shape}"

    mse = np.mean((agent_out - reference_out)**2)
    threshold = 1e-12

    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}. The output is not deterministic or incorrect."

def test_setup_py_fixed():
    path = "/app/threadpoolctl-3.1.0/setup.py"
    if os.path.isfile(path):
        with open(path, "r") as f:
            content = f.read()
        assert "improt sys" not in content, "The typo 'improt sys' is still present in /app/threadpoolctl-3.1.0/setup.py."
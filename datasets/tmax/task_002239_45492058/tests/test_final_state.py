# test_final_state.py

import os
import numpy as np
import pytest

def test_jsd_matrix_mse():
    agent_file = '/home/user/output/jsd_matrix.csv'
    ref_file = '/reference/jsd_matrix.csv'

    assert os.path.exists(agent_file), f"Agent output missing at {agent_file}"
    assert os.path.exists(ref_file), f"Reference output missing at {ref_file}. This indicates a problem with the environment setup."

    try:
        agent_matrix = np.loadtxt(agent_file, delimiter=',')
    except Exception as e:
        pytest.fail(f"Failed to load agent matrix as CSV: {e}")

    try:
        ref_matrix = np.loadtxt(ref_file, delimiter=',')
    except Exception as e:
        pytest.fail(f"Failed to load reference matrix as CSV: {e}")

    assert agent_matrix.shape == ref_matrix.shape, f"Shape mismatch: agent matrix is {agent_matrix.shape}, but reference is {ref_matrix.shape}"

    mse = np.mean((agent_matrix - ref_matrix)**2)
    assert mse <= 1e-5, f"MSE is {mse}, which is greater than the threshold of 1e-5"

def test_run_script_exists():
    script_path = '/home/user/run_analysis.sh'
    assert os.path.exists(script_path), f"Bash script missing at {script_path}"
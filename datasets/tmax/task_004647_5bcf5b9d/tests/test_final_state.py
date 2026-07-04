# test_final_state.py
import os
import subprocess
import numpy as np
import h5py
import pytest

def test_fast_prepare_mse():
    agent_script = "/home/user/fast_prepare.py"
    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."

    # Generate test data
    np.random.seed(42)
    test_raw = np.random.randn(2000, 50) @ np.random.randn(50, 50)

    test_raw_path = '/tmp/test_raw.h5'
    ref_out_path = '/tmp/reference_processed.h5'
    agent_out_path = '/home/user/test_processed.h5'

    with h5py.File(test_raw_path, 'w') as f:
        f.create_dataset('raw_features', data=test_raw)

    # Run oracle
    try:
        subprocess.run(
            ['/app/oracle_processor', test_raw_path, ref_out_path],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle processor failed to run: {e.stderr}")

    # Run agent script
    try:
        subprocess.run(
            ['python3', agent_script, test_raw_path, agent_out_path],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script failed to run: {e.stderr}")

    assert os.path.exists(agent_out_path), f"Agent output file {agent_out_path} was not created."

    # Compute metric
    with h5py.File(ref_out_path, 'r') as f:
        ref_data = f['clean_features'][:]

    with h5py.File(agent_out_path, 'r') as f:
        assert 'clean_features' in f, "Dataset 'clean_features' not found in agent's output HDF5 file."
        agent_data = f['clean_features'][:]

    assert ref_data.shape == agent_data.shape, (
        f"Shape mismatch: expected {ref_data.shape}, got {agent_data.shape}"
    )

    mse = np.mean((ref_data - agent_data)**2)
    assert mse <= 0.005, f"MSE {mse:.6f} is greater than the threshold of 0.005."
# test_final_state.py
import os
import sys
import subprocess
import pytest
import numpy as np
import h5py

def test_custom_solver_accuracy():
    agent_script = "/home/user/custom_solver.py"
    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"

    hidden_input = "/tmp/hidden_test.h5"
    oracle_output = "/tmp/oracle_out.h5"
    agent_output = "/tmp/agent_out.h5"

    # Generate hidden test data
    with h5py.File(hidden_input, "w") as f:
        for i in range(10):
            grp = f.create_group(f"system_{i}")
            # Create matrices with specific singular values including some below 0.05
            np.random.seed(42 + i)
            U, _ = np.linalg.qr(np.random.randn(20, 20))
            V, _ = np.linalg.qr(np.random.randn(20, 20))
            S = np.diag(np.linspace(0.01, 2.0, 20)) # Several < 0.05
            A = U @ S @ V.T
            b = np.random.randn(20)
            grp.create_dataset("A", data=A)
            grp.create_dataset("b", data=b)

    # Run legacy binary
    legacy_solver = "/app/bin/legacy_solver"
    assert os.path.exists(legacy_solver), f"Legacy solver missing at {legacy_solver}"

    try:
        subprocess.run([legacy_solver, hidden_input, oracle_output], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Legacy solver failed: {e.stderr}")

    # Run agent script
    try:
        subprocess.run([sys.executable, agent_script, hidden_input, agent_output], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script failed: {e.stderr}")

    assert os.path.exists(agent_output), f"Agent script did not produce output file at {agent_output}"

    # Compute metric
    max_err = 0.0
    with h5py.File(oracle_output, "r") as f_or, h5py.File(agent_output, "r") as f_ag:
        for key in f_or.keys():
            assert key in f_ag, f"Group {key} missing in agent output."
            assert "x" in f_ag[key], f"Dataset 'x' missing in group {key} of agent output."

            x_or = f_or[key]["x"][:]
            x_ag = f_ag[key]["x"][:]

            assert x_or.shape == x_ag.shape, f"Shape mismatch for {key}: expected {x_or.shape}, got {x_ag.shape}"

            err = np.max(np.abs(x_or - x_ag))
            max_err = max(max_err, err)

    assert max_err < 1e-7, f"Max Absolute Error {max_err} is not < 1e-7. The agent's custom_solver did not replicate the legacy solver accurately."
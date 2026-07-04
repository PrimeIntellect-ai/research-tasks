# test_final_state.py

import os
import subprocess
import tempfile
import struct
import numpy as np
import pytest

def generate_test_data(N, M, k1, k2, k3, noise_level=1e-4):
    """Generates synthetic transient absorption data using a simple Euler integration."""
    t = np.linspace(0, 10, N)
    dt = t[1] - t[0] if N > 1 else 0.1

    C = np.zeros((N, 4))
    C[0, 0] = 1.0

    for i in range(1, N):
        C[i, 0] = C[i-1, 0] - k1 * C[i-1, 0] * dt
        C[i, 1] = C[i-1, 1] + (k1 * C[i-1, 0] - k2 * C[i-1, 1]) * dt
        C[i, 2] = C[i-1, 2] + (k2 * C[i-1, 1] - k3 * C[i-1, 2]) * dt
        C[i, 3] = C[i-1, 3] + k3 * C[i-1, 2] * dt

    S = np.random.rand(4, M)
    Data = C @ S + np.random.randn(N, M) * noise_level

    res = struct.pack('<II', N, M)
    res += t.astype('<f8').tobytes()
    res += Data.astype('<f8').tobytes()
    return res

def read_output(filepath):
    """Reads the 3 doubles from the output binary file."""
    with open(filepath, 'rb') as f:
        data = f.read()
    if len(data) != 24:
        raise ValueError(f"Expected 24 bytes, got {len(data)}")
    return struct.unpack('<ddd', data)

@pytest.mark.parametrize("iteration", range(20))
def test_fuzz_equivalence(iteration):
    agent_executable = "/home/user/fit_model"
    oracle_executable = "/app/oracle_fit"

    assert os.path.isfile(agent_executable), f"Agent executable not found at {agent_executable}"
    assert os.access(agent_executable, os.X_OK), f"Agent executable is not executable"

    assert os.path.isfile(oracle_executable), f"Oracle executable not found at {oracle_executable}"
    assert os.access(oracle_executable, os.X_OK), f"Oracle executable is not executable"

    np.random.seed(42 + iteration)

    N = np.random.randint(20, 200)
    M = np.random.randint(20, 100)
    true_k1 = np.random.uniform(0.5, 5.0)
    true_k2 = np.random.uniform(0.5, 5.0)
    true_k3 = np.random.uniform(0.5, 5.0)

    input_data = generate_test_data(N, M, true_k1, true_k2, true_k3)

    with tempfile.NamedTemporaryFile(delete=False) as f_in, \
         tempfile.NamedTemporaryFile(delete=False) as f_out_agent, \
         tempfile.NamedTemporaryFile(delete=False) as f_out_oracle:

        f_in.write(input_data)
        f_in.flush()

        input_path = f_in.name
        agent_out_path = f_out_agent.name
        oracle_out_path = f_out_oracle.name

    try:
        # Run agent
        agent_cmd = [agent_executable, input_path, agent_out_path]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent failed with return code {agent_res.returncode}\nStderr: {agent_res.stderr}"

        # Run oracle
        oracle_cmd = [oracle_executable, input_path, oracle_out_path]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed with return code {oracle_res.returncode}\nStderr: {oracle_res.stderr}"

        agent_ks = read_output(agent_out_path)
        oracle_ks = read_output(oracle_out_path)

        for i, (ak, ok) in enumerate(zip(agent_ks, oracle_ks)):
            assert abs(ak - ok) < 1e-4, (
                f"Mismatch on k{i+1} for iteration {iteration}.\n"
                f"Agent: {agent_ks}\n"
                f"Oracle: {oracle_ks}\n"
                f"Data params: N={N}, M={M}, true_k=({true_k1:.2f}, {true_k2:.2f}, {true_k3:.2f})"
            )

    finally:
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(agent_out_path): os.remove(agent_out_path)
        if os.path.exists(oracle_out_path): os.remove(oracle_out_path)
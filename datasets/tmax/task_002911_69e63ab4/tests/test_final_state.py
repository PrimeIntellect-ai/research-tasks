# test_final_state.py

import os
import subprocess
import struct
import numpy as np
import pytest

AGENT_PROGRAM = "/home/user/truncate_lu"
ORACLE_PROGRAM = "/app/oracle_truncate_lu"
NUM_ITERATIONS = 100

def generate_diagonally_dominant_matrix(seed):
    np.random.seed(seed)
    A = np.random.uniform(-10.0, 10.0, (10, 10))
    for i in range(10):
        row_sum = np.sum(np.abs(A[i])) - np.abs(A[i, i])
        A[i, i] = np.sign(A[i, i]) * (row_sum + np.random.uniform(1.0, 10.0))
        if A[i, i] == 0:
            A[i, i] = row_sum + 1.0
    # Ensure little-endian 64-bit floats
    return A.astype('<f8').tobytes()

def test_agent_program_exists_and_executable():
    assert os.path.exists(AGENT_PROGRAM), f"Agent program {AGENT_PROGRAM} is missing."
    assert os.path.isfile(AGENT_PROGRAM), f"{AGENT_PROGRAM} is not a valid file."
    assert os.access(AGENT_PROGRAM, os.X_OK), f"Agent program {AGENT_PROGRAM} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PROGRAM), f"Oracle program {ORACLE_PROGRAM} is missing."

    for i in range(NUM_ITERATIONS):
        input_bytes = generate_diagonally_dominant_matrix(seed=42 + i)

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PROGRAM],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}."
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_PROGRAM],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        assert agent_proc.returncode == 0, f"Agent program failed on iteration {i} with error: {agent_proc.stderr.decode(errors='ignore')}"
        agent_output = agent_proc.stdout

        assert len(agent_output) == 800, f"Agent output length is {len(agent_output)} bytes, expected 800 bytes."

        # Compare outputs
        oracle_floats = np.frombuffer(oracle_output, dtype='<f8')
        agent_floats = np.frombuffer(agent_output, dtype='<f8')

        if not np.allclose(oracle_floats, agent_floats, rtol=1e-9, atol=1e-9):
            # If not close enough, fail with details
            input_floats = np.frombuffer(input_bytes, dtype='<f8').reshape(10, 10)
            diff = np.abs(oracle_floats - agent_floats)
            max_diff = np.max(diff)
            pytest.fail(
                f"Mismatch on iteration {i}.\n"
                f"Max difference: {max_diff}\n"
                f"Input matrix (first row): {input_floats[0]}\n"
                f"Oracle output (first 10): {oracle_floats[:10]}\n"
                f"Agent output (first 10): {agent_floats[:10]}"
            )
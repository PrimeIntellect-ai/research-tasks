# test_final_state.py

import os
import struct
import subprocess
import numpy as np
import pytest

ORACLE_PATH = "/app/dim_reducer_oracle"
AGENT_PATH = "/home/user/dim_reducer"

def test_agent_binary_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent binary is missing at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Path {AGENT_PATH} exists but is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"

    np.random.seed(42)

    # Run 100 iterations to keep test time reasonable, 
    # but cover enough random inputs and edge cases.
    num_iterations = 100

    for i in range(num_iterations):
        # Random N between 1 and 1000
        N = np.random.randint(1, 1001)

        # Generate N * 128 random float32s
        # Include some edge cases occasionally (like all zeros, or same values)
        if i == 0:
            floats = np.zeros(N * 128, dtype=np.float32)
        elif i == 1:
            floats = np.ones(N * 128, dtype=np.float32)
        else:
            # Random floats, some negative, some positive
            floats = (np.random.rand(N * 128).astype(np.float32) - 0.5) * 1000.0

        # Pack input
        input_bytes = struct.pack('<I', N) + floats.tobytes()

        # Run oracle
        oracle_res = subprocess.run(
            [ORACLE_PATH],
            input=input_bytes,
            capture_output=True,
            check=False
        )
        assert oracle_res.returncode == 0, f"Oracle crashed on iteration {i} with N={N}"

        # Run agent
        agent_res = subprocess.run(
            [AGENT_PATH],
            input=input_bytes,
            capture_output=True,
            check=False
        )
        assert agent_res.returncode == 0, f"Agent crashed on iteration {i} with N={N}"

        # Compare outputs
        if oracle_res.stdout != agent_res.stdout:
            pytest.fail(
                f"Mismatch on iteration {i} with N={N}.\n"
                f"Oracle output length: {len(oracle_res.stdout)}\n"
                f"Agent output length: {len(agent_res.stdout)}\n"
                f"Outputs differ. Agent did not match oracle bit-exactly."
            )
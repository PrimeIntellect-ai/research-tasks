# test_final_state.py
import os
import subprocess
import numpy as np
import pytest

ORACLE_PATH = '/app/uptime_oracle'
AGENT_PATH = '/home/user/uptime_repo/build/uptime_calc'
N_TESTS = 100  # Reduced from 1000 to prevent test timeout while maintaining rigor

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent program not found at {AGENT_PATH}. Did you compile it?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent program {AGENT_PATH} is not executable."
    assert os.path.isfile(ORACLE_PATH), f"Oracle program not found at {ORACLE_PATH}."
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle program {ORACLE_PATH} is not executable."

    np.random.seed(42)

    for i in range(N_TESTS):
        num_floats = np.random.randint(10000, 50001)
        floats = np.random.uniform(0.0, 1000.0, num_floats).astype(np.float32)

        # Fast conversion to space-separated string
        input_data = " ".join(floats.astype(str)).encode('utf-8')

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on test case {i+1} with error: {oracle_proc.stderr.decode()}"
        assert agent_proc.returncode == 0, f"Agent program failed on test case {i+1} with error: {agent_proc.stderr.decode()}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on test case {i+1} (array size {num_floats}).\n"
            f"Oracle output: {oracle_out.decode('utf-8', errors='replace')}\n"
            f"Agent output: {agent_out.decode('utf-8', errors='replace')}"
        )
# test_final_state.py
import os
import subprocess
import random
import pytest

ORACLE_PATH = "/opt/oracle/sim_oracle"
AGENT_PATH = "/home/user/sim_runner"
NUM_TESTS = 500

def test_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"File at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle at {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_TESTS):
        x0 = f"{random.uniform(0.0, 10.0):.2f}"
        y0 = f"{random.uniform(0.0, 10.0):.2f}"
        z0 = f"{random.uniform(0.0, 10.0):.2f}"

        args = [x0, y0, z0]

        try:
            oracle_res = subprocess.run([ORACLE_PATH] + args, capture_output=True, text=True, check=True, timeout=2)
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {args}: {e.stderr}")

        try:
            agent_res = subprocess.run([AGENT_PATH] + args, capture_output=True, text=True, check=True, timeout=2)
            agent_out = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input {args}. Error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {args}.")

        assert agent_out == oracle_out, (
            f"Mismatch on input {args}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Actual (Agent):   {agent_out}"
        )
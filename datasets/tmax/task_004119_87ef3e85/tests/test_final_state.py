# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_predictor"
AGENT_PATH = "/home/user/predictor"

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_oracle_executable_exists():
    assert os.path.exists(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.path.isfile(ORACLE_PATH), f"{ORACLE_PATH} is not a file"
    assert os.access(ORACLE_PATH, os.X_OK), f"{ORACLE_PATH} is not executable"

def test_fuzz_equivalence():
    test_agent_executable_exists()
    test_oracle_executable_exists()

    random.seed(42)
    num_tests = 200

    for i in range(num_tests):
        x0 = random.randint(0, 100)
        x1 = random.randint(0, 100)
        n = random.randint(2, 1000)

        args = [str(x0), str(x1), str(n)]

        oracle_cmd = [ORACLE_PATH] + args
        agent_cmd = [AGENT_PATH] + args

        oracle_result = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_result.returncode == 0, f"Oracle failed on input {args}"
        oracle_output = oracle_result.stdout.strip()

        agent_result = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_result.returncode == 0, f"Agent program failed (exit code {agent_result.returncode}) on input {args}. Stderr: {agent_result.stderr.strip()}"
        agent_output = agent_result.stdout.strip()

        assert agent_output == oracle_output, (
            f"Mismatch on input x_0={x0}, x_1={x1}, N={n}.\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output:  {agent_output}"
        )
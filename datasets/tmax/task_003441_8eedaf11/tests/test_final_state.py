# test_final_state.py
import os
import random
import subprocess
import pytest

def test_agent_executable_exists():
    agent_path = "/home/user/solver_fixed"
    assert os.path.isfile(agent_path), f"Agent executable not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent executable at {agent_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_solver"
    agent_path = "/home/user/solver_fixed"

    assert os.path.isfile(oracle_path), f"Oracle executable not found at {oracle_path}"

    random.seed(42)
    charset = " 0123456789.-"
    N = 1000

    for i in range(N):
        length = random.randint(1, 20)
        test_input = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        try:
            oracle_res = subprocess.run([oracle_path, test_input], capture_output=True, text=True, timeout=2)
            oracle_out = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            oracle_out = "TIMEOUT"

        # Run agent
        try:
            agent_res = subprocess.run([agent_path, test_input], capture_output=True, text=True, timeout=2)
            agent_out = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            agent_out = "TIMEOUT"

        assert agent_out == oracle_out, (
            f"Output mismatch on input {repr(test_input)}\n"
            f"Expected (Oracle): {repr(oracle_out)}\n"
            f"Got (Agent): {repr(agent_out)}"
        )
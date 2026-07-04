# test_final_state.py
import os
import random
import subprocess
import pytest

def test_agent_executable_exists():
    agent_path = "/home/user/new_token_gen"
    assert os.path.exists(agent_path), f"Agent program not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent program {agent_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_token_gen"
    agent_path = "/home/user/new_token_gen"

    assert os.path.exists(oracle_path), f"Oracle program not found at {oracle_path}"

    random.seed(42)
    inputs = [str(random.randint(1000, 999999)) for _ in range(500)]

    for inp in inputs:
        try:
            oracle_res = subprocess.run([oracle_path, inp], capture_output=True, text=True, timeout=2)
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {inp}")

        assert oracle_res.returncode == 0, f"Oracle failed on input {inp}"

        try:
            agent_res = subprocess.run([agent_path, inp], capture_output=True, text=True, timeout=2)
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input {inp}")

        oracle_out = oracle_res.stdout
        agent_out = agent_res.stdout

        assert agent_out == oracle_out, (
            f"Output mismatch on input {inp}.\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output: {repr(agent_out)}"
        )
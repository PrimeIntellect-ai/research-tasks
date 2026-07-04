# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_symbols():
    num_items = random.randint(1, 10)
    items = []
    for _ in range(num_items):
        length = random.randint(3, 4)
        item = ''.join(random.choices(string.ascii_uppercase, k=length))
        items.append(item)
    return ",".join(items)

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_auditor"
    agent_path = "/home/user/auditor"

    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary is not executable at {agent_path}"
    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"

    random.seed(42)

    for i in range(100):
        fuzz_input = generate_random_symbols()

        oracle_cmd = [oracle_path, fuzz_input]
        agent_cmd = [agent_path, fuzz_input]

        try:
            oracle_result = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True)
            oracle_output = oracle_result.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{fuzz_input}': {e.stderr}")

        try:
            agent_result = subprocess.run(agent_cmd, capture_output=True, text=True, check=True)
            agent_output = agent_result.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input '{fuzz_input}'. Exit code: {e.returncode}\nStderr: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Output mismatch on iteration {i+1} with input '{fuzz_input}'.\n"
            f"Expected (Oracle):\n{oracle_output}\n"
            f"Got (Agent):\n{agent_output}"
        )
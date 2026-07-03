# test_final_state.py

import os
import random
import subprocess
import string
import pytest

def test_solution_exists():
    """Verify that the user created the solution script."""
    assert os.path.isfile("/home/user/solution.py"), "Missing solution script at /home/user/solution.py"

def test_fuzz_equivalence():
    """Fuzz the agent's solution against the oracle processor."""
    oracle_path = "/app/oracle_processor"
    agent_script = "/home/user/solution.py"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle not executable at {oracle_path}"

    # 137 is the offset from the image
    env = os.environ.copy()
    env["INGESTION_OFFSET"] = "137"

    random.seed(42)
    hex_chars = "0123456789ABCDEF"

    num_tests = 5000

    for i in range(num_tests):
        length = random.randint(16, 1024)
        # Length of hex string must be even to represent bytes
        if length % 2 != 0:
            length += 1

        test_input = "".join(random.choices(hex_chars, k=length))

        # Run oracle
        oracle_cmd = [oracle_path, test_input]
        try:
            oracle_res = subprocess.run(oracle_cmd, env=env, capture_output=True, text=True, timeout=2)
            oracle_output = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {test_input}")

        # Run agent
        agent_cmd = ["/usr/bin/python3", agent_script, test_input]
        try:
            agent_res = subprocess.run(agent_cmd, env=env, capture_output=True, text=True, timeout=2)
            agent_output = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input {test_input}")

        if agent_res.returncode != 0:
            pytest.fail(f"Agent script failed with return code {agent_res.returncode} on input {test_input}.\nStderr: {agent_res.stderr}")

        assert agent_output == oracle_output, (
            f"Mismatch on input {test_input}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent):       {agent_output}"
        )
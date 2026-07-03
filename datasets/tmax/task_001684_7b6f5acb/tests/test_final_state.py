# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fuzz_equivalence():
    oracle_path = "/verify/oracle.bin"
    agent_script = "/home/user/clean_tool.py"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_!@#$"
    random.seed(42)

    for _ in range(100):
        length = random.randint(15, 50)
        test_input = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_path, test_input],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            oracle_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {test_input}: {e.stderr}")

        # Run agent script
        try:
            agent_res = subprocess.run(
                ["python3", agent_script, test_input],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            agent_output = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input '{test_input}'.\nStderr: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Mismatch on input: '{test_input}'\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )
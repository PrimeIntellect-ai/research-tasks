# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_scorer"
AGENT_PATH = "/home/user/solution"
NUM_TESTS = 1000

def test_solution_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent solution not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"

    random.seed(42)

    for _ in range(NUM_TESTS):
        args = [str(random.randint(-200, 200)) for _ in range(4)]

        try:
            oracle_res = subprocess.run(
                [ORACLE_PATH] + args,
                capture_output=True,
                text=True,
                check=True
            )
            oracle_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on inputs {args}: {e.stderr}")

        try:
            agent_res = subprocess.run(
                [AGENT_PATH] + args,
                capture_output=True,
                text=True,
                check=True
            )
            agent_output = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent solution failed on inputs {args}: {e.stderr}")

        assert agent_output == oracle_output, (
            f"Mismatch on inputs {args}.\n"
            f"Oracle output: '{oracle_output}'\n"
            f"Agent output:  '{agent_output}'"
        )
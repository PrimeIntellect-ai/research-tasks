# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/opt/oracle/user_setup"
AGENT_PATH = "/home/user/user_setup"
NUM_ITERATIONS = 50

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable"

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for i in range(NUM_ITERATIONS):
        length = random.randint(4, 15)
        test_input = ''.join(random.choice(charset) for _ in range(length))

        oracle_cmd = [ORACLE_PATH, test_input]
        agent_cmd = [AGENT_PATH, test_input]

        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, timeout=5)
            oracle_stdout = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {test_input}")
        except Exception as e:
            pytest.fail(f"Oracle failed to run on input {test_input}: {e}")

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=5)
            agent_stdout = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input: {test_input}")
        except Exception as e:
            pytest.fail(f"Agent failed to run on input {test_input}: {e}")

        assert agent_stdout == oracle_stdout, (
            f"Mismatch on input '{test_input}'\n"
            f"Expected (Oracle): {oracle_stdout!r}\n"
            f"Got (Agent): {agent_stdout!r}"
        )
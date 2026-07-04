# test_final_state.py

import os
import random
import subprocess
import pytest

def test_run_py_exists():
    assert os.path.isfile("/app/run.py"), "/app/run.py is missing. The task requires creating this file."

def test_fuzz_equivalence():
    oracle_path = "/app/oracle"
    agent_script = "/app/run.py"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle at {oracle_path} is not executable"

    random.seed(42)
    hex_chars = "0123456789ABCDEF"

    for i in range(50):
        # Even lengths between 4 and 100
        length = random.randrange(4, 101, 2)
        test_input = "".join(random.choice(hex_chars) for _ in range(length))

        # Run oracle
        try:
            oracle_result = subprocess.run(
                [oracle_path, test_input],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {test_input}: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {test_input}")

        # Run agent
        try:
            agent_result = subprocess.run(
                ["python3", agent_script, test_input],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            agent_output = agent_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {test_input}.\nReturn code: {e.returncode}\nStderr: {e.stderr}\nStdout: {e.stdout}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input {test_input}")

        assert agent_output == oracle_output, (
            f"Mismatch on input {test_input}.\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )
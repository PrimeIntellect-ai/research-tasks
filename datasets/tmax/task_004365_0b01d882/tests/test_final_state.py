# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def test_query_script_exists_and_executable():
    path = "/home/user/query.sh"
    assert os.path.exists(path), f"Missing required file: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_fuzz_equivalence():
    agent_script = "/home/user/query.sh"
    oracle = "/app/oracle_query"

    assert os.path.exists(oracle), f"Oracle missing: {oracle}"

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for i in range(200):
        length = random.randint(1, 20)
        test_input = "".join(random.choices(charset, k=length))

        # Run oracle
        try:
            oracle_result = subprocess.run([oracle, test_input], capture_output=True, text=True, timeout=5)
            oracle_output = oracle_result.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {test_input}")

        # Run agent
        try:
            agent_result = subprocess.run([agent_script, test_input], capture_output=True, text=True, timeout=5)
            agent_output = agent_result.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input: {test_input}")

        assert agent_output == oracle_output, (
            f"Output mismatch on input: '{test_input}'\n"
            f"Expected (Oracle): '{oracle_output}'\n"
            f"Actual (Agent): '{agent_output}'"
        )
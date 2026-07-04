# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_BIN = "/home/user/url_router/router_bin"
ORACLE_BIN = "/app/oracle_router"
N_TESTS = 5000
MIN_LEN = 5
MAX_LEN = 64
CHARSET = string.ascii_lowercase + string.digits + "/_-?=&"

def test_agent_binary_exists_and_executable():
    assert os.path.isfile(AGENT_BIN), f"Agent binary {AGENT_BIN} does not exist."
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary {AGENT_BIN} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_BIN), f"Oracle binary {ORACLE_BIN} missing."
    assert os.access(ORACLE_BIN, os.X_OK), f"Oracle binary {ORACLE_BIN} not executable."

    random.seed(42)

    for _ in range(N_TESTS):
        length = random.randint(MIN_LEN, MAX_LEN)
        test_input = "".join(random.choice(CHARSET) for _ in range(length))

        try:
            oracle_res = subprocess.run(
                [ORACLE_BIN, test_input],
                capture_output=True,
                text=True,
                timeout=1
            )
            oracle_stdout = oracle_res.stdout
            oracle_rc = oracle_res.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: {test_input}")

        try:
            agent_res = subprocess.run(
                [AGENT_BIN, test_input],
                capture_output=True,
                text=True,
                timeout=1
            )
            agent_stdout = agent_res.stdout
            agent_rc = agent_res.returncode
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on input: {test_input}")

        assert agent_rc == oracle_rc, (
            f"Return code mismatch for input '{test_input}'. "
            f"Expected {oracle_rc}, got {agent_rc}."
        )
        assert agent_stdout == oracle_stdout, (
            f"Stdout mismatch for input '{test_input}'.\n"
            f"Expected:\n{oracle_stdout}\n"
            f"Got:\n{agent_stdout}"
        )
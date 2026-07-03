# test_final_state.py

import os
import random
import string
import subprocess
import pytest

AGENT_BINARY = "/home/user/router_fixed"
ORACLE_BINARY = "/app/oracle_router"
NUM_ITERATIONS = 1000  # Reduced from 10000 to keep test execution time reasonable

def generate_random_url(rng):
    # Path: /[a-zA-Z0-9/]{1,1000}
    path_charset = string.ascii_letters + string.digits + "/"
    path_len = rng.randint(1, 1000)
    # Ensure it starts with /
    path = "/" + "".join(rng.choices(path_charset, k=path_len - 1)) if path_len > 1 else "/"

    # Optional params
    if rng.choice([True, False]):
        num_params = rng.randint(1, 10)
        params = []
        for _ in range(num_params):
            key_len = rng.randint(1, 20)
            key = "".join(rng.choices(string.ascii_letters + string.digits + "_", k=key_len))
            val_len = rng.randint(1, 50)
            val = "".join(rng.choices(string.ascii_letters + string.digits + "_-", k=val_len))
            params.append(f"{key}={val}")
        query = "?" + "&".join(params)
    else:
        query = ""

    return path + query

def test_router_fixed_exists():
    assert os.path.exists(AGENT_BINARY), f"Missing compiled executable: {AGENT_BINARY}"
    assert os.path.isfile(AGENT_BINARY), f"Expected {AGENT_BINARY} to be a file"
    assert os.access(AGENT_BINARY, os.X_OK), f"Expected {AGENT_BINARY} to be executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BINARY), f"Missing oracle executable: {ORACLE_BINARY}"
    assert os.access(ORACLE_BINARY, os.X_OK), f"Expected {ORACLE_BINARY} to be executable"

    rng = random.Random(42)

    for i in range(NUM_ITERATIONS):
        url = generate_random_url(rng)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_BINARY, url],
                capture_output=True,
                text=True,
                timeout=1,
                check=True
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{url}': {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input '{url}'")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_BINARY, url],
                capture_output=True,
                text=True,
                timeout=1
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Your program timed out on input '{url}'")

        assert agent_proc.returncode == 0, f"Your program crashed (return code {agent_proc.returncode}) on input '{url}'.\nStderr: {agent_proc.stderr}"

        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i+1}!\n"
                f"Input URL: {url}\n\n"
                f"Expected Output (Oracle):\n{oracle_out}\n"
                f"Actual Output (Agent):\n{agent_out}\n"
            )
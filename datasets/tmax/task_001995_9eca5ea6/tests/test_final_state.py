# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_rotator"
AGENT_PATH = "/home/user/new_rotator"
FUZZ_ITERATIONS = 1000
MIN_LEN = 8
MAX_LEN = 64

def test_agent_binary_exists_and_executable():
    """Verify that the agent has compiled the target binary and it is executable."""
    assert os.path.exists(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    """Fuzz the agent's binary against the oracle to ensure bit-exact equivalence."""
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"{ORACLE_PATH} is not executable"

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for i in range(FUZZ_ITERATIONS):
        length = random.randint(MIN_LEN, MAX_LEN)
        seed_str = "".join(random.choices(charset, k=length))

        try:
            oracle_res = subprocess.run(
                [ORACLE_PATH, seed_str],
                capture_output=True,
                text=True,
                check=True
            )
            oracle_output = oracle_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{seed_str}': {e.stderr}")

        try:
            agent_res = subprocess.run(
                [AGENT_PATH, seed_str],
                capture_output=True,
                text=True,
                check=True
            )
            agent_output = agent_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary failed on input '{seed_str}': {e.stderr}")

        assert agent_output == oracle_output, (
            f"Output mismatch on iteration {i+1}.\n"
            f"Input seed: '{seed_str}'\n"
            f"Oracle output: {repr(oracle_output)}\n"
            f"Agent output:  {repr(agent_output)}"
        )
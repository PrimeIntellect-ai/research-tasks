# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/oracle_prng"
AGENT_PATH = "/home/user/fixed_prng"
NUM_TESTS = 100

def test_fixed_prng_exists_and_executable():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle executable at {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_TESTS):
        # Generate random 64-bit unsigned integer
        seed = random.randint(0, (1 << 64) - 1)
        iterations = random.randint(100, 10000)

        seed_str = str(seed)
        iter_str = str(iterations)

        oracle_cmd = [ORACLE_PATH, seed_str, iter_str]
        agent_cmd = [AGENT_PATH, seed_str, iter_str]

        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True, timeout=5)
            oracle_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{seed_str} {iter_str}': {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input '{seed_str} {iter_str}'")

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, check=True, timeout=5)
            agent_output = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on input '{seed_str} {iter_str}': {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on input '{seed_str} {iter_str}'")

        assert agent_output == oracle_output, (
            f"Mismatch on input '{seed_str} {iter_str}'. "
            f"Oracle output: '{oracle_output}', Agent output: '{agent_output}'"
        )
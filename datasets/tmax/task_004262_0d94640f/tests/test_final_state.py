# test_final_state.py
import os
import random
import string
import subprocess
import pytest

ORACLE_BIN = "/app/legacy_calc"
AGENT_BIN = "/home/user/solution_bin"
N_TESTS = 200

def generate_random_ascii(min_len=5, max_len=500):
    length = random.randint(min_len, max_len)
    chars = string.ascii_letters + string.digits + string.punctuation + ' \n\t'
    return ''.join(random.choice(chars) for _ in range(length)).encode('utf-8')

def test_solution_bin_exists():
    assert os.path.exists(AGENT_BIN), f"Solution binary not found at {AGENT_BIN}"
    assert os.path.isfile(AGENT_BIN), f"{AGENT_BIN} is not a file"
    assert os.access(AGENT_BIN, os.X_OK), f"{AGENT_BIN} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_BIN), f"Oracle binary not found at {ORACLE_BIN}"
    assert os.access(ORACLE_BIN, os.X_OK), f"Oracle binary {ORACLE_BIN} is not executable"

    random.seed(42)

    for i in range(N_TESTS):
        input_data = generate_random_ascii()

        try:
            oracle_proc = subprocess.run(
                [ORACLE_BIN],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on input: {input_data!r}")

        try:
            agent_proc = subprocess.run(
                [AGENT_BIN],
                input=input_data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on input: {input_data!r}")

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on input {input_data!r}. "
            f"Oracle returned {oracle_proc.returncode}, Agent returned {agent_proc.returncode}"
        )

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Output mismatch on input {input_data!r}.\n"
            f"Oracle output: {oracle_proc.stdout!r}\n"
            f"Agent output: {agent_proc.stdout!r}"
        )
# test_final_state.py
import os
import random
import subprocess
import string
import pytest

ORACLE_PATH = "/app/c2_decoder"
AGENT_PATH = "/home/user/edge_decoder.sh"
N_TESTS = 500

def generate_random_hex(min_len=12, max_len=128):
    # Length must be even for valid hex strings
    length = random.choice(range(min_len, max_len + 1, 2))
    return ''.join(random.choice(string.hexdigits.lower()) for _ in range(length))

def test_agent_script_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent script {AGENT_PATH} does not exist."
    assert os.path.isfile(AGENT_PATH), f"Agent script {AGENT_PATH} is not a file."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} is missing."

    random.seed(42)  # Fixed seed for reproducibility

    for _ in range(N_TESTS):
        fuzz_input = generate_random_hex()

        # Run Oracle
        oracle_result = subprocess.run(
            [ORACLE_PATH, fuzz_input],
            capture_output=True,
            text=False,
            timeout=2
        )

        # Run Agent
        agent_result = subprocess.run(
            [AGENT_PATH, fuzz_input],
            capture_output=True,
            text=False,
            timeout=2
        )

        oracle_stdout = oracle_result.stdout
        agent_stdout = agent_result.stdout

        assert oracle_stdout == agent_stdout, (
            f"Output mismatch on input: {fuzz_input}\n"
            f"Oracle output (hex): {oracle_stdout.hex()}\n"
            f"Agent output (hex): {agent_stdout.hex()}"
        )
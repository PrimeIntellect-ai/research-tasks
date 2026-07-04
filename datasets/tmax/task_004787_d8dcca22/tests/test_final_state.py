# test_final_state.py

import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/ref_encoder"
AGENT_PATH = "/home/user/encoder"
NUM_TESTS = 500

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def generate_random_input(length):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length)) + "\n"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"{ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(NUM_TESTS):
        length = random.randint(5, 100)
        input_str = generate_random_input(length)
        input_bytes = input_str.encode('utf-8')

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {repr(input_str)}"

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if agent_proc.returncode != 0:
            pytest.fail(f"Agent program failed (exit code {agent_proc.returncode}) on input: {repr(input_str)}\nStderr: {agent_proc.stderr.decode('utf-8', errors='replace')}")

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on input: {repr(input_str)}\n"
                f"Expected (oracle): {oracle_out.hex()}\n"
                f"Got (agent):       {agent_out.hex()}"
            )
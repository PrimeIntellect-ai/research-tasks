# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_bin"
AGENT_PATH = "/home/user/deploy_tool"
NUM_TESTS = 500
MAX_LEN = 8192

def test_agent_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary is missing at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    random.seed(42)

    for i in range(NUM_TESTS):
        length = random.randint(0, MAX_LEN)
        input_data = bytes(random.choices(range(256), k=length))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_data,
                capture_output=True,
                check=False,
                timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input of length {length}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_PATH],
                input=input_data,
                capture_output=True,
                check=False,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input of length {length}")

        assert oracle_out == agent_out, (
            f"Mismatch on test {i} with input length {length}.\n"
            f"Oracle output length: {len(oracle_out)}\n"
            f"Agent output length: {len(agent_out)}\n"
            f"Oracle output (first 20 bytes): {oracle_out[:20].hex()}\n"
            f"Agent output (first 20 bytes): {agent_out[:20].hex()}"
        )
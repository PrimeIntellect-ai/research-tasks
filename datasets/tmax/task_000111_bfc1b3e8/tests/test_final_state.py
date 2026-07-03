# test_final_state.py

import os
import random
import subprocess
import string
import pytest

ORACLE_PATH = "/app/oracle_decoder"
AGENT_PATH = "/home/user/my_decoder"
MASTER_KEY = "7A9F3B2C"
N_ITERATIONS = 10000

def generate_random_hex(length_bytes):
    return ''.join(random.choices(string.hexdigits.upper(), k=length_bytes * 2))

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"{AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"{AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    random.seed(42)

    for i in range(N_ITERATIONS):
        # Random payload length between 16 and 1024 bytes
        length_bytes = random.randint(16, 1024)
        payload = generate_random_hex(length_bytes)

        # Run oracle
        oracle_cmd = [ORACLE_PATH, MASTER_KEY, payload]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on iteration {i} with payload {payload[:32]}..."
        oracle_output = oracle_res.stdout.strip()

        # Run agent
        agent_cmd = [AGENT_PATH, MASTER_KEY, payload]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent binary failed on iteration {i} with payload {payload[:32]}..."
        agent_output = agent_res.stdout.strip()

        # Compare outputs
        if oracle_output != agent_output:
            pytest.fail(
                f"Mismatch on iteration {i}!\n"
                f"Payload (first 64 chars): {payload[:64]}\n"
                f"Expected (Oracle): {oracle_output[:128]}\n"
                f"Got (Agent): {agent_output[:128]}"
            )
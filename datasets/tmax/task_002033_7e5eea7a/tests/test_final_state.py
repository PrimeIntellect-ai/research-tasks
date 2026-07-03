# test_final_state.py

import os
import sys
import json
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle/token_oracle"
AGENT_SCRIPT = "/home/user/token_rotator.py"
NUM_ITERATIONS = 100

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_hex(length):
    return ''.join(random.choices(string.hexdigits.lower(), k=length))

def generate_random_json():
    num_keys = random.randint(1, 5)
    data = {}
    for _ in range(num_keys):
        key = generate_random_string(random.randint(4, 10))
        val_type = random.choice(['int', 'string', 'hex'])
        if val_type == 'int':
            data[key] = random.randint(1, 1000000)
        elif val_type == 'string':
            data[key] = generate_random_string(random.randint(5, 20))
        else:
            data[key] = generate_random_hex(random.randint(8, 32))

    # Ensure length is somewhat controlled, but json.dumps handles it.
    return json.dumps(data)

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

    random.seed(42)

    for i in range(NUM_ITERATIONS):
        input_json = generate_random_json()

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH, input_json],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            oracle_output = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input '{input_json}'.\nStderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input '{input_json}'")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [sys.executable, AGENT_SCRIPT, input_json],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            agent_output = agent_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input '{input_json}'.\nStderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input '{input_json}'")

        assert oracle_output == agent_output, (
            f"Mismatch on iteration {i+1}!\n"
            f"Input: {input_json}\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output:  {agent_output}"
        )
# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_hex_string(length):
    return ''.join(random.choices(string.hexdigits.lower(), k=length))

def generate_payload(length):
    printable = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choices(printable, k=length))

def test_evaluate_script_exists():
    assert os.path.isfile("/home/user/evaluate.py"), "/home/user/evaluate.py is missing."

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/evaluate_reference"
    agent_script = "/home/user/evaluate.py"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle at {oracle_path} is not executable"

    # Use a fixed seed for reproducibility
    random.seed(42)

    # N=500 to prevent test timeouts while still providing robust fuzzing
    # (5000 subprocess calls to python can take several minutes)
    N = 500

    for i in range(N):
        hex_len = random.randint(2, 64) * 2  # 4 to 128 characters, even length
        bytecode_hex = generate_hex_string(hex_len)

        payload_len = random.randint(1, 256)
        payload = generate_payload(payload_len)

        # Run oracle
        oracle_cmd = [oracle_path, bytecode_hex, payload]
        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, timeout=2)
            oracle_output = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input: bytecode={bytecode_hex}, payload={payload}")

        # Run agent
        agent_cmd = ["python3", agent_script, bytecode_hex, payload]
        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=2)
            agent_output = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input: bytecode={bytecode_hex}, payload={payload}")

        assert agent_res.returncode == oracle_res.returncode, \
            f"Return code mismatch on iter {i}.\nInput: {bytecode_hex} {payload}\nOracle: {oracle_res.returncode}\nAgent: {agent_res.returncode}\nAgent stderr: {agent_res.stderr}"

        assert agent_output == oracle_output, \
            f"Output mismatch on iter {i}.\nInput: {bytecode_hex} {payload}\nOracle output: {oracle_output}\nAgent output: {agent_output}"
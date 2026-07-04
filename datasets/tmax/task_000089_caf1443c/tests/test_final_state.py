# test_final_state.py
import os
import random
import string
import subprocess
import json
import pytest

ORACLE_PATH = "/app/oracle"
AGENT_PATH = "/home/user/analyzer"
NUM_TESTS = 10000

def generate_random_string(min_len=3, max_len=15):
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_fuzz_inputs(n):
    random.seed(42)
    inputs = []
    for _ in range(n):
        r = random.random()
        if r < 0.40:
            # Valid tokens
            user = generate_random_string()
            pin = random.randint(0, 9999)
            pin_hash = pin ^ 0x5A5A
            header = json.dumps({"alg": "none"})
            payload = json.dumps({"user": user, "pin_hash": pin_hash})
            inputs.append(f"{header}|{payload}")
        elif r < 0.60:
            # Invalid algorithm
            user = generate_random_string()
            pin_hash = random.randint(0, 65535)
            alg = random.choice(["HS256", "RS256", "none ", "None", ""])
            header = json.dumps({"alg": alg})
            payload = json.dumps({"user": user, "pin_hash": pin_hash})
            inputs.append(f"{header}|{payload}")
        elif r < 0.80:
            # Malformed payload
            header = json.dumps({"alg": "none"})
            malform_type = random.randint(0, 3)
            if malform_type == 0:
                payload = json.dumps({"user": generate_random_string()}) # missing pin_hash
            elif malform_type == 1:
                payload = json.dumps({"pin_hash": random.randint(0, 65535)}) # missing user
            elif malform_type == 2:
                payload = json.dumps({"user": 123, "pin_hash": random.randint(0, 65535)}) # wrong type user
            else:
                payload = json.dumps({"user": generate_random_string(), "pin_hash": "1234"}) # wrong type pin_hash
            inputs.append(f"{header}|{payload}")
        elif r < 0.90:
            # Missing pipe character
            header = json.dumps({"alg": "none"})
            payload = json.dumps({"user": generate_random_string(), "pin_hash": random.randint(0, 65535)})
            inputs.append(f"{header}{payload}") # no pipe
        else:
            # Completely random ASCII bytes
            length = random.randint(1, 200)
            chars = [chr(random.randint(32, 126)) for _ in range(length)]
            inputs.append("".join(chars))

    return inputs

def run_binary(binary_path, input_data):
    try:
        result = subprocess.run(
            [binary_path],
            input=input_data.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1
        )
        return result.returncode, result.stdout.decode('utf-8', errors='replace')
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    inputs = generate_fuzz_inputs(NUM_TESTS)

    for i, inp in enumerate(inputs):
        oracle_code, oracle_out = run_binary(ORACLE_PATH, inp)
        agent_code, agent_out = run_binary(AGENT_PATH, inp)

        assert agent_code == oracle_code, (
            f"Exit code mismatch on input {i}:\n"
            f"Input: {inp!r}\n"
            f"Oracle code: {oracle_code}\n"
            f"Agent code: {agent_code}\n"
            f"Oracle stdout: {oracle_out!r}\n"
            f"Agent stdout: {agent_out!r}"
        )
        assert agent_out == oracle_out, (
            f"Stdout mismatch on input {i}:\n"
            f"Input: {inp!r}\n"
            f"Oracle stdout: {oracle_out!r}\n"
            f"Agent stdout: {agent_out!r}"
        )
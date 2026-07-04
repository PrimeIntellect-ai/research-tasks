# test_final_state.py

import os
import subprocess
import random
import string
import json
import base64
import hmac
import hashlib
import pytest

def b64url(data):
    if isinstance(data, str):
        data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def generate_jwt(alg, payload, secret, sig_type):
    header = {"alg": alg, "typ": "JWT"}
    hdr_b64 = b64url(json.dumps(header))
    pay_b64 = b64url(json.dumps(payload))
    msg = f"{hdr_b64}.{pay_b64}"

    if sig_type == "valid":
        sig = hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()
        sig_b64 = b64url(sig)
    elif sig_type == "garbage":
        sig_b64 = b64url(os.urandom(32))
    elif sig_type == "empty":
        sig_b64 = ""
    else:
        sig_b64 = ""

    return f"{msg}.{sig_b64}"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/policy_check_oracle"
    agent_path = "/home/user/build/policy_check"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary {agent_path} is not executable"

    random.seed(42)

    N = 10000
    inputs = []

    secret_len = random.randint(16, 64)
    secret = "".join(random.choices(string.ascii_letters + string.digits, k=secret_len))

    algs = ["HS256", "none", "RS256", "invalid"]
    roles = ["admin", "user", "guest", ""]

    for _ in range(N):
        alg = random.choice(algs)
        exp = random.choice([1600000000, 1800000000, None])
        role = random.choice(roles)
        sig_type = random.choice(["valid", "garbage", "empty"])

        payload = {}
        if exp is not None:
            payload["exp"] = exp
        if role:
            payload["role"] = role

        token = generate_jwt(alg, payload, secret, sig_type)

        # Sometimes malformed header
        if random.random() < 0.05:
            inputs.append(f"Bearer{token}")
        elif random.random() < 0.05:
            inputs.append(f"Token {token}")
        else:
            inputs.append(f"Bearer {token}")

    input_str = "\n".join(inputs) + "\n"

    try:
        oracle_proc = subprocess.run(
            [oracle_path, secret],
            input=input_str.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=True
        )
        oracle_output = oracle_proc.stdout.decode().splitlines()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed to run: {e.stderr.decode()}")

    try:
        agent_proc = subprocess.run(
            [agent_path, secret],
            input=input_str.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=True
        )
        agent_output = agent_proc.stdout.decode().splitlines()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent program failed to run: {e.stderr.decode()}")

    assert len(agent_output) == len(inputs), f"Expected {len(inputs)} lines of output, got {len(agent_output)}"

    for i in range(N):
        if agent_output[i] != oracle_output[i]:
            pytest.fail(
                f"Mismatch on input line {i+1}:\n"
                f"Input: {inputs[i]}\n"
                f"Oracle output: {oracle_output[i]}\n"
                f"Agent output: {agent_output[i]}\n"
            )
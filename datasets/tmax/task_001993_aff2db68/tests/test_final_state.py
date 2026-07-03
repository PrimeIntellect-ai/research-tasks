# test_final_state.py

import os
import subprocess
import random
import string
import itertools
import binascii
import pytest

ORACLE_PATH = "/app/token_oracle"
AGENT_PATH = "/home/user/policy_enforcer.py"
KEY = b"839201"

def encrypt_url(url: str) -> str:
    url_bytes = url.encode('ascii')
    encrypted = bytes([b ^ k for b, k in zip(url_bytes, itertools.cycle(KEY))])
    return binascii.hexlify(encrypted).decode('ascii')

def generate_random_cookie_padding() -> str:
    pad = ""
    for _ in range(random.randint(0, 3)):
        k = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
        v = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
        pad += f"{k}={v}; "
    return pad

def generate_inputs(n=1000):
    random.seed(42)
    inputs = []

    for i in range(n):
        category = i % 10

        prefix = generate_random_cookie_padding()
        suffix = generate_random_cookie_padding()

        if category < 2:
            # 20% without redirect_token
            cookie = prefix + suffix
        elif category < 4:
            # 20% with invalid hex
            invalid_hex = ''.join(random.choices("ghijklmnopqrstuvwxyz", k=10))
            cookie = f"{prefix}redirect_token={invalid_hex}; {suffix}"
        elif category < 7:
            # 30% valid hex, trusted domain
            path = ''.join(random.choices(string.ascii_letters + string.digits + "/", k=random.randint(0, 20)))
            url = f"https://trusted.corp.local/{path}"
            hex_token = encrypt_url(url)
            cookie = f"{prefix}redirect_token={hex_token}; {suffix}"
        else:
            # 30% valid hex, untrusted domain
            domain = random.choice([
                "http://evil.com/",
                "https://trusted.corp.local.evil.com/",
                "https://other.local/",
                "http://trusted.corp.local/"
            ])
            path = ''.join(random.choices(string.ascii_letters + string.digits + "/", k=random.randint(0, 20)))
            url = f"{domain}{path}"
            hex_token = encrypt_url(url)
            cookie = f"{prefix}redirect_token={hex_token}; {suffix}"

        inputs.append(cookie)

    return inputs

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"

    inputs = generate_inputs(1000)

    for idx, cookie in enumerate(inputs):
        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH, cookie],
                capture_output=True,
                text=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout.strip()
        except Exception as e:
            pytest.fail(f"Oracle failed to run on input {idx}: {e}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", AGENT_PATH, cookie],
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_out = agent_proc.stdout.strip()
        except Exception as e:
            pytest.fail(f"Agent script failed to run on input {idx}: {e}")

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on input {idx}!\n"
                f"Input Cookie: {cookie}\n"
                f"Oracle Output: {oracle_out}\n"
                f"Agent Output:  {agent_out}\n"
            )
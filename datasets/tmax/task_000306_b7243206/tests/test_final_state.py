# test_final_state.py

import os
import stat
import json
import base64
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_bin"
AGENT_PATH = "/home/user/jwt_processor"
PRIVATE_KEY_PATH = "/app/private_key.pem"
N_FUZZ = 200

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def sign_rsa(data: bytes, key_path: str) -> bytes:
    p = subprocess.run(
        ['openssl', 'dgst', '-sha256', '-sign', key_path],
        input=data, capture_output=True, check=True
    )
    return p.stdout

def generate_jwt(kind: str) -> str:
    if kind == 'valid':
        header = {"alg": "RS256", "typ": "JWT"}
    elif kind == 'none':
        header = {"alg": random.choice(["none", "NONE", "NoNe"])}
    else:
        header = {"alg": "RS256", "typ": "JWT"}

    payload = {}
    if random.choice([True, False]):
        payload["email"] = ''.join(random.choices(string.ascii_lowercase, k=10)) + "@example.com"
    if random.choice([True, False]):
        payload["phone"] = "".join(random.choices(string.digits, k=10))
    if random.choice([True, False]):
        payload["other"] = ''.join(random.choices(string.ascii_letters, k=8))

    header_b64 = b64url_encode(json.dumps(header, separators=(',', ':')).encode())
    payload_b64 = b64url_encode(json.dumps(payload, separators=(',', ':')).encode())

    signing_input = f"{header_b64}.{payload_b64}".encode()

    if kind == 'none':
        # Add random stripped signature or none
        if random.choice([True, False]):
            return f"{header_b64}.{payload_b64}."
        else:
            return f"{header_b64}.{payload_b64}"

    sig = sign_rsa(signing_input, PRIVATE_KEY_PATH)

    if kind == 'invalid_sig':
        # tamper signature by flipping the last byte
        sig = sig[:-1] + bytes([sig[-1] ^ 0xFF])

    sig_b64 = b64url_encode(sig)
    return f"{header_b64}.{payload_b64}.{sig_b64}"

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent script {AGENT_PATH} does not exist."
    st = os.stat(AGENT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Agent script {AGENT_PATH} is not executable."

def test_oracle_exists():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} does not exist."
    st = os.stat(ORACLE_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Oracle binary {ORACLE_PATH} is not executable."

def test_fuzz_equivalence():
    random.seed(42)

    kinds = (
        ['valid'] * int(N_FUZZ * 0.4) +
        ['none'] * int(N_FUZZ * 0.3) +
        ['invalid_sig'] * int(N_FUZZ * 0.3)
    )
    random.shuffle(kinds)

    for i, kind in enumerate(kinds):
        jwt_str = generate_jwt(kind)

        # Run oracle
        p_oracle = subprocess.run(
            [ORACLE_PATH],
            input=jwt_str.encode(),
            capture_output=True
        )

        # Run agent
        p_agent = subprocess.run(
            [AGENT_PATH],
            input=jwt_str.encode(),
            capture_output=True
        )

        assert p_agent.returncode == p_oracle.returncode, (
            f"Exit code mismatch on input {i} (kind: {kind}).\n"
            f"Input JWT: {jwt_str}\n"
            f"Oracle exit code: {p_oracle.returncode}\n"
            f"Agent exit code: {p_agent.returncode}\n"
            f"Oracle stdout: {p_oracle.stdout.decode(errors='replace')}\n"
            f"Agent stdout: {p_agent.stdout.decode(errors='replace')}\n"
            f"Agent stderr: {p_agent.stderr.decode(errors='replace')}"
        )

        assert p_agent.stdout == p_oracle.stdout, (
            f"Stdout mismatch on input {i} (kind: {kind}).\n"
            f"Input JWT: {jwt_str}\n"
            f"Oracle stdout: {p_oracle.stdout.decode(errors='replace')!r}\n"
            f"Agent stdout: {p_agent.stdout.decode(errors='replace')!r}\n"
            f"Agent stderr: {p_agent.stderr.decode(errors='replace')}"
        )
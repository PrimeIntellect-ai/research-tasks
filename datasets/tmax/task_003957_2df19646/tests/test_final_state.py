# test_final_state.py

import os
import random
import subprocess
import json
import base64
import hmac
import hashlib
import pytest

ORACLE_PATH = "/app/jwt_oracle"
AGENT_SCRIPT = "/home/user/verify.sh"
SECRET_KEY = b"b4sh_s3cr3t_99"

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode('ascii')

def create_jwt(header: dict, payload: dict, secret: bytes = None, sign: bool = True) -> str:
    header_enc = b64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_enc = b64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
    msg = f"{header_enc}.{payload_enc}"

    if not sign:
        return f"{msg}."

    if secret is None:
        secret = SECRET_KEY

    sig = hmac.new(secret, msg.encode('utf-8'), hashlib.sha256).digest()
    sig_enc = b64url_encode(sig)
    return f"{msg}.{sig_enc}"

def generate_test_cases(n=500):
    random.seed(42)
    cases = []

    payload = {"user": "admin", "role": "superuser"}

    for _ in range(n // 4):
        # 1. Valid JWTs
        cases.append(create_jwt({"alg": "HS256", "typ": "JWT"}, payload, secret=SECRET_KEY))

        # 2. alg: none
        alg_none = random.choice(["none", "NONE", "nOnE", "NoNe"])
        cases.append(create_jwt({"alg": alg_none, "typ": "JWT"}, payload, sign=False))

        # 3. Invalid key
        bad_key = b"wrong_secret_" + bytes([random.randint(0, 255)])
        cases.append(create_jwt({"alg": "HS256", "typ": "JWT"}, payload, secret=bad_key))

        # 4. Malformed
        malformed_types = [
            "just.two.parts.wait.four",
            "not.even.base64!",
            "",
            "$(echo bad)",
            "`rm -rf /`",
            create_jwt({"alg": "HS256"}, payload) + "bad",
            "..."
        ]
        cases.append(random.choice(malformed_types))

    random.shuffle(cases)
    return cases

def run_cmd(cmd, arg):
    try:
        result = subprocess.run([cmd, arg], capture_output=True, text=True, timeout=2)
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", -1
    except Exception as e:
        return str(e), -2

def test_script_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"

    test_cases = generate_test_cases(500)

    for i, case in enumerate(test_cases):
        oracle_out, oracle_code = run_cmd(ORACLE_PATH, case)
        agent_out, agent_code = run_cmd(AGENT_SCRIPT, case)

        assert agent_code == oracle_code, (
            f"Exit code mismatch on input {i}:\n"
            f"Input: {case}\n"
            f"Oracle code: {oracle_code}\n"
            f"Agent code: {agent_code}\n"
            f"Oracle out: {oracle_out}\n"
            f"Agent out: {agent_out}"
        )

        assert agent_out == oracle_out, (
            f"Stdout mismatch on input {i}:\n"
            f"Input: {case}\n"
            f"Oracle out: {oracle_out}\n"
            f"Agent out: {agent_out}"
        )
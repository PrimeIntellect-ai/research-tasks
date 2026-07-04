# test_final_state.py

import os
import glob
import json
import base64
import hmac
import hashlib
import random
import subprocess
import string
import pytest

def test_logs_redacted():
    """Verify that the secret is removed from all logs and replaced with [REDACTED]."""
    log_files = glob.glob("/home/user/logs/*.log")
    assert len(log_files) > 0, "No log files found in /home/user/logs/"

    for log_file in log_files:
        with open(log_file, "r") as f:
            content = f.read()

        assert "PURPLE_ELEPHANT_42" not in content, f"Secret 'PURPLE_ELEPHANT_42' still found in {log_file}"

        # We know auth.log and app.log originally contained the secret, so they must now contain [REDACTED]
        if os.path.basename(log_file) in ["auth.log", "app.log"]:
            assert "[REDACTED]" in content, f"[REDACTED] not found in {log_file}"

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def generate_jwt(header: dict, payload: dict, secret: str) -> str:
    h = b64url_encode(json.dumps(header).encode('utf-8'))
    p = b64url_encode(json.dumps(payload).encode('utf-8'))
    msg = f"{h}.{p}".encode('utf-8')
    sig = b64url_encode(hmac.new(secret.encode('utf-8'), msg, hashlib.sha256).digest())
    return f"{h}.{p}.{sig}"

def test_jwt_validator_fuzzing():
    """Fuzz the agent's JWT validator against the reference oracle."""
    agent_script = "/home/user/jwt_validator.py"
    oracle_script = "/app/reference_validator_oracle.py"

    assert os.path.exists(agent_script), f"Agent script {agent_script} not found"
    assert os.path.exists(oracle_script), f"Oracle script {oracle_script} not found"

    random.seed(42)
    secret = "SUPER_SECRET_" + "".join(random.choices(string.ascii_letters, k=10))
    wrong_secret = "WRONG_SECRET_" + "".join(random.choices(string.ascii_letters, k=10))

    cases = []

    # 25% valid HS256 tokens signed with the provided random secret
    for _ in range(250):
        payload = {"user": "admin", "id": random.randint(1, 1000)}
        cases.append(generate_jwt({"alg": "HS256", "typ": "JWT"}, payload, secret))

    # 25% alg=none tokens
    for _ in range(250):
        alg = random.choice(["none", "None", "NONE", "nOnE"])
        payload = {"user": "admin", "id": random.randint(1, 1000)}
        h = b64url_encode(json.dumps({"alg": alg, "typ": "JWT"}).encode('utf-8'))
        p = b64url_encode(json.dumps(payload).encode('utf-8'))
        cases.append(f"{h}.{p}.")

    # 25% valid HS256 tokens but signed with the WRONG secret
    for _ in range(250):
        payload = {"user": "admin", "id": random.randint(1, 1000)}
        cases.append(generate_jwt({"alg": "HS256", "typ": "JWT"}, payload, wrong_secret))

    # 15% malformed JWTs
    for _ in range(150):
        cases.append("".join(random.choices(string.ascii_letters + string.digits + ".", k=50)))

    # 10% HS256 tokens with modified payloads but original signatures
    for _ in range(100):
        payload = {"user": "admin", "id": random.randint(1, 1000)}
        valid_jwt = generate_jwt({"alg": "HS256", "typ": "JWT"}, payload, secret)
        h, p, s = valid_jwt.split('.')
        bad_p = b64url_encode(json.dumps({"user": "hacker", "id": 9999}).encode('utf-8'))
        cases.append(f"{h}.{bad_p}.{s}")

    random.shuffle(cases)

    for i, token in enumerate(cases):
        # Run oracle
        oracle_proc = subprocess.run(
            ["python3", oracle_script, "--secret", secret],
            input=token, text=True, capture_output=True
        )
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script, "--secret", secret],
            input=token, text=True, capture_output=True
        )
        agent_out = agent_proc.stdout.strip()

        assert agent_proc.returncode == 0, f"Agent script exited with non-zero code {agent_proc.returncode} on input {token}\nStderr: {agent_proc.stderr}"

        try:
            oracle_json = json.loads(oracle_out)
        except json.JSONDecodeError:
            oracle_json = oracle_out

        try:
            agent_json = json.loads(agent_out)
        except json.JSONDecodeError:
            pytest.fail(f"Agent output is not valid JSON. Output: {agent_out}")

        assert agent_json == oracle_json, f"Mismatch on case {i}.\nToken: {token}\nOracle output: {oracle_out}\nAgent output: {agent_out}"
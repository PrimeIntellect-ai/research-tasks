# test_final_state.py

import os
import subprocess
import json
import base64
import hmac
import hashlib
import random
import string
import pytest

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')

def generate_jwt(alg="HS256", payload_data="", secret=b"SECRET_KEY_9988776655", invalid_sig=False, missing_sig=False):
    header = {"alg": alg, "typ": "JWT"}
    payload = {"data": payload_data}

    h_b64 = b64url_encode(json.dumps(header, separators=(',', ':')).encode())
    p_b64 = b64url_encode(json.dumps(payload, separators=(',', ':')).encode())

    msg = f"{h_b64}.{p_b64}".encode()
    if alg.lower() == "none":
        sig = b""
    else:
        sig = hmac.new(secret, msg, hashlib.sha256).digest()

    if invalid_sig:
        sig = (sig + b"invalid")[:len(sig)] if sig else b"invalid"

    if missing_sig:
        s_b64 = ""
    else:
        s_b64 = b64url_encode(sig)

    return f"{h_b64}.{p_b64}.{s_b64}"

def test_secure_auth_exists():
    assert os.path.isfile("/home/user/secure_auth.py"), "secure_auth.py not found at /home/user/secure_auth.py"

def test_nginx_config_updated():
    with open("/app/nginx/nginx.conf", "r") as f:
        content = f.read()
    assert "eyJhbGciOiJub25lIg" in content, "Nginx config does not contain the IDS regex for 'alg':'none'"

def test_start_services_updated():
    with open("/app/start_services.sh", "r") as f:
        content = f.read()
    assert "bwrap" in content, "bwrap command not found in start_services.sh"
    assert "secure_auth.py" in content, "secure_auth.py not found in start_services.sh"
    assert "legacy_auth" not in content, "legacy_auth should be removed from start_services.sh"

def test_fuzz_equivalence():
    random.seed(42)
    oracle_path = "/app/bin/legacy_auth"
    agent_script = "/home/user/secure_auth.py"

    # Run 1000 iterations to avoid excessive test time while still providing good coverage
    N = 1000

    for _ in range(N):
        length = random.randint(10, 50)
        payload_data = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        choice = random.random()
        alg = "HS256"
        invalid_sig = False
        missing_sig = False

        if choice < 0.1:
            alg = "none"
        elif choice < 0.2:
            alg = "None"
        elif choice < 0.4:
            invalid_sig = True
        elif choice < 0.5:
            missing_sig = True

        token = generate_jwt(alg=alg, payload_data=payload_data, invalid_sig=invalid_sig, missing_sig=missing_sig)

        # Run agent
        try:
            agent_res = subprocess.run(
                ["python3", agent_script, token],
                capture_output=True,
                text=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on token: {token}")

        is_none_alg = alg.lower() == "none"

        if is_none_alg:
            # Agent MUST reject
            assert agent_res.returncode == 1, f"Agent script did not return exit code 1 for alg=none token: {token}"
            assert "invalid_algorithm" in agent_res.stdout or "invalid_algorithm" in agent_res.stderr, f"Agent script did not output 'invalid_algorithm' for alg=none token: {token}"
        else:
            # Run oracle
            oracle_res = subprocess.run(
                [oracle_path, token],
                capture_output=True,
                text=True
            )
            assert agent_res.stdout == oracle_res.stdout, f"Mismatch on token {token}.\nOracle: {oracle_res.stdout}\nAgent: {agent_res.stdout}"
            assert agent_res.returncode == oracle_res.returncode, f"Exit code mismatch on token {token}.\nOracle: {oracle_res.returncode}\nAgent: {agent_res.returncode}"
# test_final_state.py

import os
import json
import base64
import hmac
import hashlib
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def base64url_encode(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def create_jwt(payload, secret, alg="HS256"):
    header = {"typ": "JWT", "alg": alg}
    encoded_header = base64url_encode(json.dumps(header))
    encoded_payload = base64url_encode(json.dumps(payload))
    msg = f"{encoded_header}.{encoded_payload}"

    if alg == "none":
        return f"{msg}."
    elif alg == "HS256":
        sig = hmac.new(secret.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).digest()
        return f"{msg}.{base64url_encode(sig)}"
    else:
        raise ValueError("Unsupported alg")

def test_secret_file():
    secret_path = "/home/user/jwt_secret.txt"
    assert os.path.exists(secret_path), f"Secret file {secret_path} does not exist."
    with open(secret_path, "r") as f:
        secret = f.read().strip()
    assert secret == "4928", f"Secret file contains incorrect secret: {secret}"

def test_certificates_exist():
    cert_path = "/home/user/cert.pem"
    key_path = "/home/user/key.pem"
    assert os.path.exists(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.exists(key_path), f"Key file {key_path} does not exist."

def test_audit_log_endpoint():
    url = "https://127.0.0.1:8443/audit/log"
    log_path = "/home/user/audit.log"

    # 1. Test valid HS256 JWT
    payload1 = {"username": "admin", "cc_number": "1111222233334444", "event": "login"}
    jwt1 = create_jwt({}, "4928", alg="HS256") # using empty payload in JWT, but wait, the spec says "Valid requests will contain a JSON payload".
    # Actually, the payload is typically in the request body, not necessarily the JWT payload, but usually JWTs carry it.
    # The prompt says: "Valid requests will contain a JSON payload with the following structure". This implies the request body is JSON.
    # Let's send it in the request body.

    headers1 = {"Authorization": f"Bearer {jwt1}", "Content-Type": "application/json"}
    try:
        resp1 = requests.post(url, json=payload1, headers=headers1, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to {url}: {e}"

    assert resp1.status_code == 200, f"Expected HTTP 200 for valid JWT, got {resp1.status_code}"

    assert os.path.exists(log_path), f"Audit log {log_path} was not created."
    with open(log_path, "r") as f:
        logs = f.read()
    assert "[admin] login - ****-****-****-4444" in logs, "Audit log missing or incorrect for valid request."

    # 2. Test alg=none Vulnerability
    payload2 = {"username": "hacker", "cc_number": "9999888877776666", "event": "data_dump"}
    jwt2 = create_jwt({}, "4928", alg="none")
    headers2 = {"Authorization": f"Bearer {jwt2}", "Content-Type": "application/json"}
    resp2 = requests.post(url, json=payload2, headers=headers2, verify=False, timeout=5)

    assert resp2.status_code == 200, f"Expected HTTP 200 for alg=none JWT, got {resp2.status_code}"

    with open(log_path, "r") as f:
        logs = f.read()
    assert "[hacker] data_dump - ****-****-****-6666" in logs, "Audit log missing or incorrect for alg=none request."

    # 3. Test Invalid Signature
    payload3 = {"username": "thief", "cc_number": "1234123412341234", "event": "steal"}
    jwt3 = create_jwt({}, "0000", alg="HS256")
    headers3 = {"Authorization": f"Bearer {jwt3}", "Content-Type": "application/json"}
    resp3 = requests.post(url, json=payload3, headers=headers3, verify=False, timeout=5)

    assert resp3.status_code == 401, f"Expected HTTP 401 for invalid JWT signature, got {resp3.status_code}"

    with open(log_path, "r") as f:
        logs = f.read()
    assert "[thief]" not in logs, "Audit log should not contain entry for unauthorized request."
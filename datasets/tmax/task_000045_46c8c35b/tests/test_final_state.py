# test_final_state.py

import os
import socket
import hashlib
import subprocess
import hmac
import pytest

def get_suid_hash():
    suspicious_dir = "/home/user/suspicious"
    for f in os.listdir(suspicious_dir):
        path = os.path.join(suspicious_dir, f)
        if os.path.isfile(path) and (os.stat(path).st_mode & 0o4000):
            with open(path, "rb") as f_in:
                return hashlib.sha256(f_in.read()).hexdigest()
    return None

def get_attacker_ip():
    with open("/home/user/access.log", "r", encoding="utf-8") as f:
        for line in f:
            if "X-Exploit-Payload" in line:
                return line.split()[0]
    return None

def get_c2_secret():
    try:
        out = subprocess.check_output(
            ["ffmpeg", "-i", "/app/evidence.mp4", "-f", "srt", "-"],
            stderr=subprocess.DEVNULL
        ).decode(errors="ignore")
        for line in out.splitlines():
            if "C2_SECRET:" in line:
                return line.split("C2_SECRET:")[1].strip()
    except Exception:
        pass
    return None

def send_raw_http_request(auth_header=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(("127.0.0.1", 8080))
        req = "GET /audit HTTP/1.1\r\nHost: 127.0.0.1\r\n"
        if auth_header is not None:
            req += f"X-Incident-Auth: {auth_header}\r\n"
        req += "\r\n"
        s.sendall(req.encode("utf-8"))

        resp = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp += chunk
                # If we have a body or just headers, we can break early if it looks complete
                # But since it's a simple bash server, connection might close or just hang.
                if b"\r\n\r\n" in resp and len(resp) > 200:
                    break
            except socket.timeout:
                break
        return resp.decode("utf-8", errors="ignore")
    finally:
        s.close()

@pytest.fixture(scope="module")
def truth_data():
    suid_hash = get_suid_hash()
    ip = get_attacker_ip()
    secret = get_c2_secret()

    assert suid_hash is not None, "Could not find SUID binary to compute hash"
    assert ip is not None, "Could not find attacker IP in access.log"
    assert secret is not None, "Could not extract C2_SECRET from video"

    expected_hmac = hmac.new(secret.encode(), ip.encode(), hashlib.sha256).hexdigest()

    return {
        "hash": suid_hash,
        "hmac": expected_hmac
    }

def test_webhook_valid_token(truth_data):
    response = send_raw_http_request(auth_header=truth_data["hmac"])
    assert response, "Received empty response from webhook for valid request"
    assert "200 OK" in response, f"Expected 200 OK for valid token, got: {response[:100]}"
    assert truth_data["hash"] in response, f"Expected SUID hash {truth_data['hash']} in response, got: {response}"

def test_webhook_invalid_token():
    response = send_raw_http_request(auth_header="deadbeef1234567890abcdef")
    assert response, "Received empty response from webhook for invalid token"
    assert "403 Forbidden" in response, f"Expected 403 Forbidden for invalid token, got: {response[:100]}"

def test_webhook_missing_token():
    response = send_raw_http_request(auth_header=None)
    assert response, "Received empty response from webhook for missing token"
    assert "403 Forbidden" in response, f"Expected 403 Forbidden for missing token, got: {response[:100]}"
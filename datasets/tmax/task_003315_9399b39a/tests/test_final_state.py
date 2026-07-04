# test_final_state.py
import subprocess
import requests
import pytest

URL = "http://127.0.0.1:8080/inspect"
TOKEN = "omega7delta"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def make_dummy_cert(domain: str) -> str:
    cmd = [
        "openssl", "req", "-x509", "-newkey", "rsa:2048",
        "-keyout", "/dev/null", "-out", "/dev/stdout",
        "-sha256", "-days", "1", "-nodes",
        "-subj", f"/CN={domain}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.DEVNULL)
    return result.stdout

def test_unauthorized():
    try:
        r = requests.post(URL, json={})
    except requests.exceptions.ConnectionError:
        pytest.fail("Server is not listening on 127.0.0.1:8080")

    assert r.status_code == 401, f"Expected 401 Unauthorized, got {r.status_code}"

    r2 = requests.post(URL, headers={"Authorization": "Bearer wrongtoken"}, json={})
    assert r2.status_code == 401, f"Expected 401 Unauthorized for wrong token, got {r2.status_code}"

def test_blocked_domain():
    cert = make_dummy_cert("evilcorp.local")
    payload = {
        "domain": "evilcorp.local",
        "cert_chain_pem": cert,
        "payload": "normal payload",
        "user_agent": "Mozilla/5.0"
    }
    r = requests.post(URL, headers=HEADERS, json=payload)
    assert r.status_code == 200, f"Expected 200 OK, got {r.status_code}"

    data = r.json()
    assert data.get("status") == "blocked_domain", f"Expected status 'blocked_domain', got {data.get('status')}"

def test_invalid_cert():
    cert = make_dummy_cert("wrongsite.com")
    payload = {
        "domain": "goodsite.com",
        "cert_chain_pem": cert,
        "payload": "normal payload",
        "user_agent": "Mozilla/5.0"
    }
    r = requests.post(URL, headers=HEADERS, json=payload)
    assert r.status_code == 200, f"Expected 200 OK, got {r.status_code}"

    data = r.json()
    assert data.get("status") == "invalid_cert", f"Expected status 'invalid_cert', got {data.get('status')}"

def test_blocked_injection():
    cert = make_dummy_cert("goodsite.com")
    payload = {
        "domain": "goodsite.com",
        "cert_chain_pem": cert,
        "payload": "normal payload",
        "user_agent": "Mozilla/5.0 ' OR 1=1 --"
    }
    r = requests.post(URL, headers=HEADERS, json=payload)
    assert r.status_code == 200, f"Expected 200 OK, got {r.status_code}"

    data = r.json()
    assert data.get("status") == "blocked_injection", f"Expected status 'blocked_injection', got {data.get('status')}"

def test_allowed_and_redaction():
    cert = make_dummy_cert("goodsite.com")
    payload = {
        "domain": "goodsite.com",
        "cert_chain_pem": cert,
        "payload": "Payment 1234567812345678 received and another 9876543210987654.",
        "user_agent": "Mozilla/5.0"
    }
    r = requests.post(URL, headers=HEADERS, json=payload)
    assert r.status_code == 200, f"Expected 200 OK, got {r.status_code}"

    data = r.json()
    assert data.get("status") == "allowed", f"Expected status 'allowed', got {data.get('status')}"
    assert data.get("redacted_payload") == "Payment XXXX-XXXX-XXXX-XXXX received and another XXXX-XXXX-XXXX-XXXX.", \
        f"Payload redaction failed, got: {data.get('redacted_payload')}"
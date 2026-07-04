# test_final_state.py

import os
import subprocess
import requests
import pytest

def test_generate_key_script():
    script_path = "/home/user/generate_key.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    # Clean up any existing keys to ensure the script generates them
    for f in ["/home/user/admin_key", "/home/user/admin_key.pub"]:
        if os.path.exists(f):
            os.remove(f)

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"generate_key.sh failed with output: {result.stderr}"

    pub_key_path = "/home/user/admin_key.pub"
    assert os.path.isfile(pub_key_path), f"Public key {pub_key_path} was not generated"

    with open(pub_key_path, "r") as f:
        pub_key_content = f.read()

    assert "CORP_SEC_2024_AUTH" in pub_key_content, "The secret identifier CORP_SEC_2024_AUTH is missing from the public key comment"

def test_login_redirect_valid():
    url = "http://127.0.0.1:8080/cgi-bin/login.sh?next=/dashboard"
    try:
        resp = requests.get(url, allow_redirects=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 302, f"Expected 302, got {resp.status_code}. Response: {resp.text}"
    assert resp.headers.get("Location") == "/dashboard", f"Expected Location: /dashboard, got {resp.headers.get('Location')}"

def test_login_redirect_invalid_domain():
    url = "http://127.0.0.1:8080/cgi-bin/login.sh?next=http://evil.com"
    try:
        resp = requests.get(url, allow_redirects=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 302, f"Expected 302, got {resp.status_code}. Response: {resp.text}"
    assert resp.headers.get("Location") == "/index.sh", f"Expected Location: /index.sh for invalid redirect, got {resp.headers.get('Location')}"

def test_login_redirect_invalid_double_slash():
    url = "http://127.0.0.1:8080/cgi-bin/login.sh?next=//evil.com"
    try:
        resp = requests.get(url, allow_redirects=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 302, f"Expected 302, got {resp.status_code}. Response: {resp.text}"
    assert resp.headers.get("Location") == "/index.sh", f"Expected Location: /index.sh for double slash redirect, got {resp.headers.get('Location')}"

def test_diag_valid_ip():
    url = "http://127.0.0.1:8080/cgi-bin/diag.sh?ip=127.0.0.1"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}. Response: {resp.text}"
    assert "127.0.0.1" in resp.text and ("ping" in resp.text.lower() or "bytes from" in resp.text.lower()), "Expected ping output in response"

def test_diag_invalid_ip():
    url = "http://127.0.0.1:8080/cgi-bin/diag.sh?ip=127.0.0.1;id"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 400, f"Expected 400 Bad Request for invalid IP, got {resp.status_code}. Response: {resp.text}"
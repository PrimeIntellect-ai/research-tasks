# test_final_state.py

import os
import re
import subprocess
import pytest
import requests
import urllib3

# Disable insecure request warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_cracked_password_file():
    """Verify that the cracked password was correctly identified and written."""
    path = "/home/user/cracked_password.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "Secure_7382", f"Expected 'Secure_7382', but found '{content}' in {path}"

def test_certificate_exists_and_cn():
    """Verify the TLS certificate exists and has the correct Common Name."""
    cert_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"
    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Private key file {key_path} is missing."

    result = subprocess.run(
        ["openssl", "x509", "-noout", "-subject", "-in", cert_path],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to read certificate: {result.stderr}"
    assert "CN = honeypot.local" in result.stdout or "CN=honeypot.local" in result.stdout, \
        f"Certificate does not have Common Name 'honeypot.local'. Subject: {result.stdout.strip()}"

def test_honeypot_process_state():
    """Verify the honeypot process is listening, chrooted, and running as nobody."""
    # Find process listening on TCP 8443
    res = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True)
    pid = None
    for line in res.stdout.splitlines():
        if ":8443" in line and "LISTEN" in line:
            m = re.search(r'pid=(\d+)', line)
            if m:
                pid = m.group(1)
                break

    assert pid is not None, "No process found listening on port 8443."

    # Verify process is running as nobody (UID 65534)
    proc_stat_path = f"/proc/{pid}"
    assert os.path.isdir(proc_stat_path), f"Process directory {proc_stat_path} does not exist."
    uid = os.stat(proc_stat_path).st_uid
    assert uid == 65534, f"Process {pid} is running as UID {uid}, expected 65534 (nobody)."

    # Verify process is chrooted to /home/user/jail
    root_link = os.readlink(f"/proc/{pid}/root")
    assert root_link == "/home/user/jail", f"Process {pid} is chrooted to {root_link}, expected /home/user/jail."

def test_https_valid_request():
    """Verify the honeypot grants access with the correct cookie."""
    url = "https://127.0.0.1:8443/"
    cookies = {"AuthToken": "Secure_7382"}
    try:
        r = requests.get(url, cookies=cookies, verify=False, timeout=5)
        assert r.status_code == 200, f"Expected HTTP 200 OK, got {r.status_code}"
        assert "ACCESS GRANTED" in r.text, f"Expected 'ACCESS GRANTED' in response body, got '{r.text}'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Valid HTTPS request failed: {e}")

def test_https_invalid_request():
    """Verify the honeypot denies access with an incorrect cookie."""
    url = "https://127.0.0.1:8443/"
    cookies = {"AuthToken": "Secure_1111"}
    try:
        r = requests.get(url, cookies=cookies, verify=False, timeout=5)
        assert r.status_code == 403, f"Expected HTTP 403 Forbidden, got {r.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Invalid HTTPS request failed: {e}")

def test_https_no_cookie():
    """Verify the honeypot denies access when no cookie is provided."""
    url = "https://127.0.0.1:8443/"
    try:
        r = requests.get(url, verify=False, timeout=5)
        assert r.status_code == 403, f"Expected HTTP 403 Forbidden, got {r.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"No-cookie HTTPS request failed: {e}")
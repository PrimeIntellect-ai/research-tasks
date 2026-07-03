# test_final_state.py

import os
import stat
import hmac
import hashlib
import subprocess
import pytest

def test_tls_certificate_exists_and_valid():
    cert_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"

    assert os.path.exists(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.exists(key_path), f"Key file {key_path} does not exist."

    # Check Common Name using openssl
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout", "-subject"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to parse certificate: {result.stderr}"
    assert "CN = secure-legacy.local" in result.stdout or "CN=secure-legacy.local" in result.stdout, \
        f"Certificate does not have the correct Common Name (CN). Got: {result.stdout}"

def test_auth_token_generation():
    secret_path = "/home/user/secret.txt"
    token_path = "/home/user/auth_token.txt"

    assert os.path.exists(token_path), f"Token file {token_path} does not exist."

    with open(secret_path, "r") as f:
        secret = f.read().strip()

    expected_hmac = hmac.new(
        secret.encode('utf-8'),
        b"user=admin",
        hashlib.sha256
    ).hexdigest()

    with open(token_path, "r") as f:
        actual_token = f.read().strip()

    assert actual_token == expected_hmac, f"Auth token does not match expected HMAC. Expected {expected_hmac}, got {actual_token}"

def test_audit_report_contents():
    report_path = "/home/user/audit_report.txt"
    assert os.path.exists(report_path), f"Audit report {report_path} does not exist."

    expected_files = [
        "/home/user/app/subdir/another_suid",
        "/home/user/app/suid_bin",
        "/home/user/app/world_writable.log"
    ]

    with open(report_path, "r") as f:
        actual_files = [line.strip() for line in f if line.strip()]

    assert actual_files == expected_files, f"Audit report contents are incorrect. Expected {expected_files}, got {actual_files}"

def test_run_secure_wrapper():
    wrapper_path = "/home/user/run_secure.sh"
    assert os.path.exists(wrapper_path), f"Wrapper script {wrapper_path} does not exist."

    st = os.stat(wrapper_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Wrapper script {wrapper_path} is not executable."

    with open(wrapper_path, "r") as f:
        content = f.read()

    assert "ulimit -n 50" in content, "Wrapper script does not contain 'ulimit -n 50'."
    assert "env -i" in content, "Wrapper script does not contain 'env -i'."
    assert "PATH=/usr/bin:/bin" in content or "PATH='/usr/bin:/bin'" in content or 'PATH="/usr/bin:/bin"' in content, \
        "Wrapper script does not set PATH correctly."
    assert "AUTH_TOKEN" in content, "Wrapper script does not expose AUTH_TOKEN."
    assert "/home/user/app/server.py" in content, "Wrapper script does not execute the target server script."
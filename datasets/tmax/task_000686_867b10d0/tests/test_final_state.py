# test_final_state.py

import os
import subprocess
import urllib.request
import ssl
import pytest

def test_phase1_password_recovery():
    """Verify that the cracked password is saved correctly."""
    pass_file = "/app/config/admin_pass.txt"
    assert os.path.isfile(pass_file), f"Password file not found at {pass_file}"

    with open(pass_file, "r") as f:
        password = f.read().strip()

    assert password == "admin123", f"Incorrect password in {pass_file}. Expected 'admin123', got '{password}'"

def test_phase2_tls_certs_exist():
    """Verify that the TLS certificates were generated."""
    cert_file = "/app/certs/cert.pem"
    key_file = "/app/certs/key.pem"

    assert os.path.isfile(cert_file), f"Certificate file not found at {cert_file}"
    assert os.path.isfile(key_file), f"Private key file not found at {key_file}"

def test_phase2_nginx_running_and_proxying():
    """Verify that Nginx is listening on 8443 with TLS and proxying to the backend."""
    url = "https://127.0.0.1:8443/ping"

    # Create an unverified SSL context to allow self-signed certificates
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            status = response.getcode()
            assert status == 200, f"Expected HTTP 200 from {url}, got {status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx on {url}. Is it running and configured for TLS? Error: {e}")

def test_phase3_sanitizer_exists():
    """Verify that the sanitizer binary exists and is executable."""
    binary_path = "/home/user/sanitizer"
    assert os.path.isfile(binary_path), f"Sanitizer binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Sanitizer binary at {binary_path} is not executable"

def test_phase3_adversarial_corpus():
    """Verify the sanitizer against the clean and evil corpora."""
    binary_path = "/home/user/sanitizer"
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_payloads = os.listdir(evil_dir)
    clean_payloads = os.listdir(clean_dir)

    evil_bypassed = []
    clean_rejected = []

    # Test evil corpus
    for payload in evil_payloads:
        result = subprocess.run([binary_path, payload], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(payload)

    # Test clean corpus
    for payload in clean_payloads:
        result = subprocess.run([binary_path, payload], capture_output=True)
        if result.returncode != 0:
            clean_rejected.append(payload)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_payloads)} evil bypassed: {evil_bypassed}")
    if clean_rejected:
        error_msgs.append(f"{len(clean_rejected)} of {len(clean_payloads)} clean modified/rejected: {clean_rejected}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))
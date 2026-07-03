# test_final_state.py

import os
import socket
import subprocess
import requests
import pytest

def test_http_service_normal():
    """Verify the HTTP service is running, returns the correct body, and includes the CSP header."""
    try:
        resp = requests.get('http://127.0.0.1:8000/evidence', timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service on 127.0.0.1:8000: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}"
    assert resp.text.strip() == "Evidence Secure", f"Expected body 'Evidence Secure', got '{resp.text}'"

    csp = resp.headers.get('Content-Security-Policy')
    assert csp == "default-src 'self'", f"Expected CSP header \"default-src 'self'\", got '{csp}'"

def test_http_service_backdoor_removed():
    """Verify the backdoor has been successfully removed and does not execute arbitrary commands."""
    trigger_file = '/tmp/backdoor_triggered'
    if os.path.exists(trigger_file):
        os.remove(trigger_file)

    headers = {
        'Cookie': 'Session-Id=admin_debug_mode',
        'X-System-Debug': f'touch {trigger_file}'
    }

    try:
        resp = requests.get('http://127.0.0.1:8000/evidence', headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP service during backdoor test: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code} when sending backdoor payload"
    assert not os.path.exists(trigger_file), "The backdoor was triggered! The file /tmp/backdoor_triggered was created."

def test_ssh_service_up():
    """Verify an SSH service is listening on port 2222."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect(('127.0.0.1', 2222))
        banner = s.recv(1024)
        assert b'SSH' in banner, f"Service on port 2222 did not return an SSH banner. Got: {banner}"
    except socket.error as e:
        pytest.fail(f"Failed to connect to SSH service on 127.0.0.1:2222: {e}")
    finally:
        s.close()

def test_ssh_password_auth_disabled():
    """Verify that password authentication is disabled or fails for the user 'analyst'."""
    cmd = [
        'ssh', 
        '-o', 'StrictHostKeyChecking=no', 
        '-o', 'UserKnownHostsFile=/dev/null',
        '-o', 'PasswordAuthentication=yes', 
        '-o', 'PubkeyAuthentication=no',
        '-o', 'BatchMode=yes', 
        '-p', '2222', 
        'analyst@127.0.0.1', 
        'echo', 'hello'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode != 0, "SSH password authentication succeeded, but it should be strictly disabled."

def test_ssh_random_key_auth_fails(tmp_path):
    """Verify that authentication with an unauthorized SSH key fails for the user 'analyst'."""
    key_path = tmp_path / "id_rsa"
    subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '2048', '-f', str(key_path), '-N', ''], check=True, capture_output=True)

    cmd = [
        'ssh', 
        '-o', 'StrictHostKeyChecking=no', 
        '-o', 'UserKnownHostsFile=/dev/null',
        '-o', 'IdentitiesOnly=yes', 
        '-o', 'PasswordAuthentication=no',
        '-o', 'BatchMode=yes',
        '-i', str(key_path), 
        '-p', '2222', 
        'analyst@127.0.0.1', 
        'echo', 'hello'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode != 0, "SSH key authentication succeeded with a random key, but it should only accept the recovered key."
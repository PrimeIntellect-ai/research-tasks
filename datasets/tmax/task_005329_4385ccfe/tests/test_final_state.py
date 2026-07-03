# test_final_state.py

import os
import subprocess
import json
import pytest

def test_auth_svc_binary():
    """Test the C microservice source, binary, and output."""
    c_file = "/home/user/auth_svc.c"
    bin_file = "/home/user/auth_svc"

    assert os.path.isfile(c_file), f"{c_file} does not exist."
    assert os.path.isfile(bin_file), f"{bin_file} does not exist."
    assert os.access(bin_file, os.X_OK), f"{bin_file} is not executable."

    result = subprocess.run([bin_file], capture_output=True, text=False)
    assert result.returncode == 0, "auth_svc execution failed."

    expected_output = b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"status":"healthy","service":"auth-service"}\n'
    assert result.stdout == expected_output, "auth_svc output does not match the exact expected HTTP response."

def test_tls_configuration():
    """Test the TLS server setup and response."""
    crt_file = "/home/user/server.crt"
    key_file = "/home/user/server.key"

    assert os.path.isfile(crt_file), f"{crt_file} does not exist."
    assert os.path.isfile(key_file), f"{key_file} does not exist."

    # Check if port 8443 is listening and responds properly
    try:
        result = subprocess.run(
            ["curl", "-s", "-k", "https://localhost:8443"],
            capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0, "curl to https://localhost:8443 failed."
        assert '{"status":"healthy","service":"auth-service"}' in result.stdout, "Unexpected response from TLS server."
    except subprocess.TimeoutExpired:
        pytest.fail("Timeout while trying to connect to TLS server on port 8443.")

def test_ssh_tunneling():
    """Test SSH key generation, authorization, and tunneling."""
    ssh_dir = "/home/user/.ssh"
    priv_key = os.path.join(ssh_dir, "id_ed25519")
    pub_key = os.path.join(ssh_dir, "id_ed25519.pub")
    auth_keys = os.path.join(ssh_dir, "authorized_keys")

    assert os.path.isfile(priv_key), f"{priv_key} does not exist."
    assert os.path.isfile(pub_key), f"{pub_key} does not exist."
    assert os.path.isfile(auth_keys), f"{auth_keys} does not exist."

    with open(pub_key, "r") as f:
        pub_key_content = f.read().strip()

    with open(auth_keys, "r") as f:
        auth_keys_content = f.read()

    assert pub_key_content in auth_keys_content, "Public key is not in authorized_keys."

    # Check if port 9090 is listening and responds properly via the tunnel
    try:
        result = subprocess.run(
            ["curl", "-s", "-k", "https://localhost:9090"],
            capture_output=True, text=True, timeout=5
        )
        assert result.returncode == 0, "curl to https://localhost:9090 failed."
        assert '{"status":"healthy","service":"auth-service"}' in result.stdout, "Unexpected response from SSH tunnel."
    except subprocess.TimeoutExpired:
        pytest.fail("Timeout while trying to connect to SSH tunnel on port 9090.")

def test_monitoring_daemon():
    """Test the monitoring daemon script and its output log."""
    script_file = "/home/user/monitor.sh"
    log_file = "/home/user/health_log.txt"

    assert os.path.isfile(script_file), f"{script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"{script_file} is not executable."

    assert os.path.isfile(log_file), f"{log_file} does not exist."

    with open(log_file, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) >= 3, f"Expected at least 3 lines in {log_file}, found {len(lines)}."

    expected_line = '{"status":"healthy","service":"auth-service"}'
    for i, line in enumerate(lines):
        assert line == expected_line, f"Line {i+1} in {log_file} does not match expected JSON. Got: {line}"
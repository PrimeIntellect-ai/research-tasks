# test_final_state.py

import os
import stat
import subprocess
import urllib.request
import ssl
import pytest

def test_mounted_logs():
    """Verify that the squashfs archive is mounted and readable."""
    auth1_path = "/home/user/mnt_logs/auth1.log"
    assert os.path.isfile(auth1_path), f"{auth1_path} does not exist. Archive might not be mounted."

    with open(auth1_path, "r") as f:
        content = f.read()
    assert "Accepted password" in content, "Expected content not found in mounted log file."

def test_generate_alerts_script():
    """Verify that generate_alerts.sh exists and is executable."""
    script_path = "/home/user/generate_alerts.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_alerts_generated():
    """Verify that ssh_alerts.txt is generated and contains the correct lines."""
    alerts_path = "/home/user/alerts/ssh_alerts.txt"
    assert os.path.isfile(alerts_path), f"{alerts_path} does not exist."

    with open(alerts_path, "r") as f:
        lines = [line.strip() for line in f if "Failed publickey" in line]

    assert len(lines) == 2, f"Expected exactly 2 lines containing 'Failed publickey', found {len(lines)}."

    content = "\n".join(lines)
    assert "Jan 14 10:05:22 server sshd[1235]: Failed publickey" in content
    assert "Jan 14 10:07:11 server sshd[1236]: Silent rejection: Failed publickey" in content

def test_acl_permissions():
    """Verify that user 'nobody' has read access via ACL."""
    alerts_path = "/home/user/alerts/ssh_alerts.txt"
    assert os.path.isfile(alerts_path), f"{alerts_path} does not exist."

    result = subprocess.run(["getfacl", alerts_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run getfacl."

    acl_lines = result.stdout.splitlines()
    has_nobody_read = any(line.startswith("user:nobody:r") for line in acl_lines)
    assert has_nobody_read, f"ACL for {alerts_path} does not grant read permission to 'nobody'."

def test_tls_certificates():
    """Verify that the TLS certificate and key exist."""
    cert_path = "/home/user/cert.pem"
    key_path = "/home/user/key.pem"

    assert os.path.isfile(cert_path), f"Certificate {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Private key {key_path} does not exist."

def test_serve_script():
    """Verify that serve.sh exists and is executable."""
    script_path = "/home/user/serve.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_web_server_running():
    """Verify that the web server is running on port 8443 and serving the alerts over HTTPS."""
    url = "https://127.0.0.1:8443/ssh_alerts.txt"

    # Create an unverified SSL context to accept self-signed certificates
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=context, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP status 200, got {response.status}."
            content = response.read().decode('utf-8')
            assert "Failed publickey" in content, "The served file does not contain the expected text."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the HTTPS server on port 8443: {e}")
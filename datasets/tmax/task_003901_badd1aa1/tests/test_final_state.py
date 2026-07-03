# test_final_state.py

import os
import stat
import subprocess
import requests
import re
import socket
import time

def test_http_headers_and_cookies():
    # Wait for service to be up
    for _ in range(10):
        try:
            resp = requests.get("http://127.0.0.1:8080/", timeout=2)
            break
        except requests.RequestException:
            time.sleep(1)
    else:
        assert False, "Nginx service on port 8080 is not reachable."

    headers = {k.lower(): v for k, v in resp.headers.items()}

    assert "x-frame-options" in headers, "X-Frame-Options header is missing."
    assert headers["x-frame-options"].upper() == "DENY", f"X-Frame-Options is {headers['x-frame-options']}, expected DENY."

    assert "x-content-type-options" in headers, "X-Content-Type-Options header is missing."
    assert headers["x-content-type-options"].lower() == "nosniff", f"X-Content-Type-Options is {headers['x-content-type-options']}, expected nosniff."

    assert "set-cookie" in headers, "Set-Cookie header is missing."
    cookie_val = headers["set-cookie"].lower()
    assert "secure" in cookie_val, "Set-Cookie does not contain the Secure flag."
    assert "httponly" in cookie_val, "Set-Cookie does not contain the HttpOnly flag."

def test_ssh_password_auth_rejected():
    # Attempt SSH connection with password authentication
    cmd = [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-o", "BatchMode=yes",
        "-o", "PreferredAuthentications=password",
        "-p", "2222",
        "user@127.0.0.1"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # BatchMode=yes prevents password prompt, so it will fail immediately if password is the only option
    # It should fail with "Permission denied"
    assert result.returncode != 0, "SSH connection with password authentication succeeded, but it should be disabled."
    assert "Permission denied" in result.stderr or "Connection closed" in result.stderr or "publickey" in result.stderr, \
        f"Expected password authentication to be rejected, got: {result.stderr}"

def test_ssh_ciphers_restricted():
    # Use nmap to enumerate supported ciphers
    cmd = ["nmap", "--script", "ssh2-enum-algos", "-p", "2222", "127.0.0.1"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        # Fallback if nmap is not installed: parse sshd_config
        with open("/home/user/app/ssh/sshd_config", "r") as f:
            config = f.read()
        ciphers_line = re.search(r"^\s*Ciphers\s+(.+)$", config, re.MULTILINE)
        assert ciphers_line, "Ciphers directive not found in sshd_config."
        ciphers = ciphers_line.group(1).split(",")
        allowed_ciphers = {"chacha20-poly1305@openssh.com", "aes256-gcm@openssh.com"}
        for c in ciphers:
            assert c.strip() in allowed_ciphers, f"Disallowed cipher found: {c.strip()}"
        return

    output = result.stdout
    if "ssh2-enum-algos" in output:
        # Extract ciphers section
        ciphers_section = re.search(r"encryption_algorithms:(.*?)mac_algorithms:", output, re.DOTALL)
        if ciphers_section:
            ciphers_text = ciphers_section.group(1)
            ciphers = re.findall(r"\s+([a-zA-Z0-9\-@.]+)", ciphers_text)
            allowed_ciphers = {"chacha20-poly1305@openssh.com", "aes256-gcm@openssh.com"}
            for c in ciphers:
                assert c in allowed_ciphers, f"SSH server supports disallowed cipher: {c}"
            assert len(ciphers) > 0, "No ciphers found in nmap output."
        else:
            # Fallback to checking the config if nmap output parsing fails
            pass

def test_system_state():
    key_path = "/home/user/app/ssh/ssh_host_ed25519_key"
    assert os.path.exists(key_path), f"{key_path} does not exist."
    mode = os.stat(key_path).st_mode
    assert stat.S_IMODE(mode) == 0o600, f"Permissions of {key_path} are {oct(stat.S_IMODE(mode))}, expected 0600."

    scan_script = "/home/user/scan.sh"
    assert os.path.isfile(scan_script), f"{scan_script} does not exist."
    assert os.access(scan_script, os.X_OK), f"{scan_script} is not executable."

    assert os.path.isfile("/home/user/pre_report.txt"), "/home/user/pre_report.txt does not exist."
    assert os.path.isfile("/home/user/post_report.txt"), "/home/user/post_report.txt does not exist."
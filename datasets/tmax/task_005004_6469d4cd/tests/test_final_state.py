# test_final_state.py
import os
import pty
import json
import time
import pytest
import requests

def test_http_report():
    url = "http://127.0.0.1:8080/report.json"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except Exception as e:
        pytest.fail(f"Failed to connect to HTTP server or fetch {url}: {e}")

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response from {url} is not valid JSON. Content: {resp.text}")

    expected_ip = "172.16.4.88"
    expected_password = "B@ckD00r_77Xq"

    assert data.get("attacker_ip") == expected_ip, f"Expected attacker_ip '{expected_ip}', got '{data.get('attacker_ip')}'"
    assert data.get("backdoor_password") == expected_password, f"Expected backdoor_password '{expected_password}', got '{data.get('backdoor_password')}'"

def test_ssh_honeypot():
    try:
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect("127.0.0.1", port=8022, username="admin", password="B@ckD00r_77Xq", timeout=5)
            client.close()
        except Exception as e:
            pytest.fail(f"SSH connection failed using paramiko: {e}")
        return
    except ImportError:
        pass

    # Fallback to using pty and ssh binary if paramiko is not installed
    pid, fd = pty.fork()
    if pid == 0:
        # Child: run ssh
        os.execvp("ssh", [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            "-o", "PubkeyAuthentication=no",
            "-p", "8022",
            "admin@127.0.0.1",
            "echo success"
        ])
    else:
        # Parent: interact with ssh
        output = b""
        password_sent = False
        try:
            while True:
                data = os.read(fd, 1024)
                if not data:
                    break
                output += data
                if b"password:" in output.lower() and not password_sent:
                    os.write(fd, b"B@ckD00r_77Xq\n")
                    password_sent = True
        except OSError:
            pass # EIO when child exits

        _, status = os.waitpid(pid, 0)
        output_str = output.decode(errors='ignore')

        if "Permission denied" in output_str:
            pytest.fail(f"SSH authentication failed. Output:\n{output_str}")

        if not password_sent and "success" not in output_str:
            pytest.fail(f"SSH connection failed or did not prompt for password. Output:\n{output_str}")
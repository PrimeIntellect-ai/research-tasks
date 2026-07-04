# test_final_state.py

import os
import socket
import subprocess
import time
import pytest

def test_forensics_report_exists():
    """Check that the forensics report was created."""
    path = "/home/user/forensics_report.txt"
    assert os.path.exists(path), f"Missing forensics report at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_secure_uploader_binary():
    """Check that the secure uploader was compiled."""
    path = "/home/user/secure_uploader"
    assert os.path.exists(path), f"Missing secure uploader binary at {path}"
    assert os.access(path, os.X_OK), f"Secure uploader at {path} is not executable"

def test_custom_daemon_valid_upload():
    """Test that the custom daemon accepts valid uploads."""
    host, port = "127.0.0.1", 8080
    filename = "evidence1.txt"
    content = b"test_evidence_data"

    # Ensure vault exists
    vault_dir = "/home/user/evidence_vault"
    if not os.path.exists(vault_dir):
        os.makedirs(vault_dir, exist_ok=True)

    target_file = os.path.join(vault_dir, filename)
    if os.path.exists(target_file):
        os.remove(target_file)

    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(f"STORE {filename}\n".encode() + content)
    except Exception as e:
        pytest.fail(f"Failed to connect or send data to daemon on {host}:{port}: {e}")

    time.sleep(0.5) # Wait for daemon to write

    assert os.path.exists(target_file), f"Daemon did not write to {target_file}"
    with open(target_file, "rb") as f:
        assert f.read() == content, "File content does not match uploaded data"

def test_custom_daemon_path_traversal():
    """Test that the custom daemon rejects path traversal."""
    host, port = "127.0.0.1", 8080
    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(b"STORE ../../../etc/shadow\nmalicious_data")
            response = s.recv(1024)
            assert response == b"ERROR: INVALID PATH\n", f"Expected ERROR: INVALID PATH\\n, got {response}"
    except Exception as e:
        pytest.fail(f"Failed during path traversal test: {e}")

def test_custom_daemon_backdoor():
    """Test that the custom daemon rejects the backdoor filename."""
    host, port = "127.0.0.1", 8080
    try:
        with socket.create_connection((host, port), timeout=2) as s:
            s.sendall(b"STORE sys_update_bin\nmalicious_data")
            response = s.recv(1024)
            assert response == b"ERROR: INVALID PATH\n", f"Expected ERROR: INVALID PATH\\n, got {response}"
    except Exception as e:
        pytest.fail(f"Failed during backdoor test: {e}")

def test_ssh_configuration():
    """Check SSH configuration for port 2222 and pubkey auth."""
    # Check if SSH is listening on 2222
    try:
        with socket.create_connection(("127.0.0.1", 2222), timeout=2) as s:
            banner = s.recv(1024)
            assert b"SSH" in banner, "Service on port 2222 does not appear to be SSH"
    except Exception as e:
        pytest.fail(f"Failed to connect to SSH on port 2222: {e}")

    # Check authorized_keys
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.exists(auth_keys_path), "authorized_keys file not found"

    with open("/home/user/investigator.pub", "r") as f:
        pub_key = f.read().strip()

    with open(auth_keys_path, "r") as f:
        auth_keys = f.read()

    assert pub_key in auth_keys, "Investigator public key not found in authorized_keys"

def test_iptables_rules():
    """Check iptables rules for INPUT DROP, lo ACCEPT, and TCP 2222 ACCEPT."""
    try:
        result = subprocess.run(["iptables", "-S"], capture_output=True, text=True, check=True)
        rules = result.stdout

        assert "-P INPUT DROP" in rules, "Default INPUT policy is not DROP"
        assert "-A INPUT -i lo -j ACCEPT" in rules or "-A INPUT -i lo -m comment" in rules or any("lo" in r and "ACCEPT" in r for r in rules.splitlines() if "-A INPUT" in r), "Loopback interface not explicitly allowed in INPUT"
        assert "-p tcp" in rules and "2222" in rules and "ACCEPT" in rules, "TCP port 2222 not explicitly allowed in INPUT"

    except FileNotFoundError:
        pytest.fail("iptables command not found")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run iptables: {e.stderr}")
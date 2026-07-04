# test_final_state.py

import os
import re
import pytest

def test_attacker_ip():
    """Verify that the attacker IP was correctly identified."""
    ip_file = "/home/user/attacker_ip.txt"
    assert os.path.isfile(ip_file), f"Missing file: {ip_file}"

    with open(ip_file, "r") as f:
        ip = f.read().strip()

    assert ip == "10.13.37.100", f"Incorrect attacker IP in {ip_file}. Found: {ip}"

def test_new_payload():
    """Verify that the new payload was correctly crafted using the discovered XOR key."""
    payload_file = "/home/user/new_payload.bin"
    assert os.path.isfile(payload_file), f"Missing file: {payload_file}"

    with open(payload_file, "rb") as f:
        payload = f.read()

    expected_command = "cat /etc/passwd"
    expected_payload = bytes([ord(c) ^ 0x55 for c in expected_command])

    assert payload == expected_payload, f"Payload in {payload_file} does not match the expected XOR'd bytes."

def test_block_attacker_script():
    """Verify the firewall script contains the correct iptables command."""
    script_file = "/home/user/block_attacker.sh"
    assert os.path.isfile(script_file), f"Missing file: {script_file}"

    with open(script_file, "r") as f:
        content = f.read().strip()

    # Check for required iptables components
    assert "iptables" in content, "iptables command not found in script."
    assert "-A INPUT" in content or "--append INPUT" in content, "Rule must be appended to the INPUT chain."
    assert "-p tcp" in content or "--protocol tcp" in content, "Rule must specify TCP protocol."
    assert "-s 10.13.37.100" in content or "--source 10.13.37.100" in content, "Rule must specify the attacker's source IP."
    assert "--dport 7777" in content or "--destination-port 7777" in content, "Rule must specify destination port 7777."
    assert "-j DROP" in content or "--jump DROP" in content, "Rule must DROP the traffic."
    assert "sudo" not in content, "Script must not use sudo."

def test_ssh_key_generated():
    """Verify the Ed25519 SSH key was generated correctly."""
    key_file = "/home/user/admin_key"
    assert os.path.isfile(key_file), f"Missing file: {key_file}"

    with open(key_file, "r") as f:
        content = f.read()

    assert "BEGIN OPENSSH PRIVATE KEY" in content, f"{key_file} does not appear to be a valid OpenSSH private key."

def test_hardened_sshd_config():
    """Verify the hardened SSH configuration contains the required settings."""
    config_file = "/home/user/hardened_sshd_config"
    assert os.path.isfile(config_file), f"Missing file: {config_file}"

    with open(config_file, "r") as f:
        lines = f.readlines()

    # Strip comments and whitespace
    active_settings = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = re.split(r'\s+', line, maxsplit=1)
        if len(parts) == 2:
            active_settings[parts[0].lower()] = parts[1].lower()

    assert active_settings.get("passwordauthentication") == "no", "PasswordAuthentication must be set to 'no'."
    assert active_settings.get("permitrootlogin") == "no", "PermitRootLogin must be set to 'no'."
    assert active_settings.get("x11forwarding") == "no", "X11Forwarding must be set to 'no'."
    assert active_settings.get("protocol") == "2", "Protocol must be explicitly set to '2'."
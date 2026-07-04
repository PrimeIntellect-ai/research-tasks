# test_final_state.py

import os
import re
import pytest

def test_remediation_dir_exists():
    path = "/home/user/remediation"
    assert os.path.isdir(path), f"The directory {path} does not exist. Did you create it?"

def test_blocked_ips_txt():
    path = "/home/user/remediation/blocked_ips.txt"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ips = {"192.168.1.100", "10.0.0.5"}
    actual_ips = set(lines)

    assert actual_ips == expected_ips, (
        f"The file {path} does not contain the correct IPs. "
        f"Expected {expected_ips}, but found {actual_ips}."
    )
    assert len(lines) == 2, f"The file {path} should contain exactly 2 lines, but found {len(lines)}."

def test_block_sh():
    path = "/home/user/remediation/block.sh"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    expected_commands = [
        "iptables -A INPUT -s 192.168.1.100 -j DROP",
        "iptables -A INPUT -s 10.0.0.5 -j DROP"
    ]

    for cmd in expected_commands:
        assert cmd in content, (
            f"The required iptables command '{cmd}' was not found in {path}."
        )

def test_sshd_config_secure():
    path = "/home/user/remediation/sshd_config_secure"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, "r") as f:
        lines = f.readlines()

    permit_root_login_no = False
    password_auth_no = False

    for line in lines:
        stripped = line.strip()
        # Ignore comments
        if stripped.startswith("#"):
            continue

        # Check for PermitRootLogin
        if re.search(r"^\s*PermitRootLogin\s+yes", stripped, re.IGNORECASE):
            pytest.fail(f"Found active 'PermitRootLogin yes' in {path}. It should be set to 'no'.")
        if re.search(r"^\s*PermitRootLogin\s+no", stripped, re.IGNORECASE):
            permit_root_login_no = True

        # Check for PasswordAuthentication
        if re.search(r"^\s*PasswordAuthentication\s+yes", stripped, re.IGNORECASE):
            pytest.fail(f"Found active 'PasswordAuthentication yes' in {path}. It should be set to 'no'.")
        if re.search(r"^\s*PasswordAuthentication\s+no", stripped, re.IGNORECASE):
            password_auth_no = True

    assert permit_root_login_no, f"'PermitRootLogin no' was not found as an active configuration in {path}."
    assert password_auth_no, f"'PasswordAuthentication no' was not found as an active configuration in {path}."
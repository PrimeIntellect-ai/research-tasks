# test_final_state.py

import os
import pytest

def test_auth_conf_updated():
    """Verify that auth.conf was updated to use password authentication."""
    auth_file = "/home/user/appliance_fs/auth.conf"
    assert os.path.exists(auth_file), f"{auth_file} does not exist."

    with open(auth_file, "r") as f:
        content = f.read()

    assert "auth_type=password" in content, "auth.conf does not contain 'auth_type=password'."

def test_network_conf_contents():
    """Verify that network.conf contains the correct interface and route configuration."""
    net_file = "/home/user/appliance_fs/network.conf"
    assert os.path.exists(net_file), f"{net_file} does not exist. Did the expect script run successfully?"

    with open(net_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "interface=vlan20 192.168.100.1/24",
        "route=10.0.0.0/8 192.168.100.254"
    ]

    for expected in expected_lines:
        assert expected in lines, f"network.conf is missing expected line: '{expected}'"

def test_deploy_log_success():
    """Verify that deploy.log contains the success message."""
    log_file = "/home/user/deploy.log"
    assert os.path.exists(log_file), f"{log_file} does not exist. The commit command may not have been executed."

    with open(log_file, "r") as f:
        content = f.read().strip()

    assert content == "DEPLOYMENT_SUCCESS", f"deploy.log does not contain the exact success message. Found: '{content}'"

def test_expect_script_exists():
    """Verify that the expect script was created."""
    script_file = "/home/user/auto_deploy.exp"
    assert os.path.exists(script_file), f"Expect script {script_file} does not exist."
    assert os.path.isfile(script_file), f"{script_file} is not a regular file."
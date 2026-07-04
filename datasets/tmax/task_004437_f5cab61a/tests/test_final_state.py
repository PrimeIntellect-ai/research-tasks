# test_final_state.py

import os
import re
import subprocess
import pytest

def test_sshd_config_exists_and_configured():
    """Test that sshd_config exists and contains the required hardening settings."""
    config_path = "/home/user/sshd_config"
    assert os.path.isfile(config_path), f"{config_path} does not exist"

    with open(config_path, "r") as f:
        content = f.read()

    # Check for Port 2222
    assert re.search(r'(?i)^\s*Port\s+2222\b', content, re.MULTILINE), "Port 2222 not configured in sshd_config"

    # Check for PasswordAuthentication no
    assert re.search(r'(?i)^\s*PasswordAuthentication\s+no\b', content, re.MULTILINE), "PasswordAuthentication no not configured in sshd_config"

    # Check for PubkeyAuthentication yes (or it's default, but task says explicitly enable)
    assert re.search(r'(?i)^\s*PubkeyAuthentication\s+yes\b', content, re.MULTILINE), "PubkeyAuthentication yes not configured in sshd_config"

    # Check for HostKey
    assert re.search(r'(?i)^\s*HostKey\s+/home/user/ssh_host_ed25519_key\b', content, re.MULTILINE), "HostKey /home/user/ssh_host_ed25519_key not configured in sshd_config"

def test_sshd_running():
    """Test that sshd is running with the custom config."""
    try:
        output = subprocess.check_output(["ps", "aux"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ps aux")

    assert "/home/user/sshd_config" in output, "sshd is not running with -f /home/user/sshd_config"

def test_loot_txt_exists_and_correct():
    """Test that loot.txt exists and contains the correct string."""
    loot_path = "/home/user/loot.txt"
    assert os.path.isfile(loot_path), f"{loot_path} does not exist"

    with open(loot_path, "r") as f:
        content = f.read()

    assert content.strip() == "ACCESS_GRANTED", f"{loot_path} does not contain the expected text 'ACCESS_GRANTED'"

def test_secure_runner_exists():
    """Test that secure_runner.py exists."""
    runner_path = "/home/user/secure_runner.py"
    assert os.path.isfile(runner_path), f"{runner_path} does not exist"

def test_authorized_keys_exists():
    """Test that authorized_keys exists."""
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"{auth_keys_path} does not exist"
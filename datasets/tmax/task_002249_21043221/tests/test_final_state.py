# test_final_state.py

import os
import re
import pytest

def test_c_code_fixed():
    """Verify that daemon.c has been modified to include setlocale and tzset."""
    file_path = "/home/user/daemon.c"
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    assert "setlocale" in content, "daemon.c does not contain 'setlocale'."
    assert "tzset" in content, "daemon.c does not contain 'tzset'."

def test_daemon_binary_compiled():
    """Verify that daemon binary is compiled and executable."""
    binary_path = "/home/user/daemon"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_launch_script():
    """Verify the launch script start.sh exists, is executable, and has correct content."""
    script_path = "/home/user/start.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "TZ=Asia/Tokyo" in content, "start.sh does not set TZ=Asia/Tokyo."
    assert "LC_ALL=ja_JP.UTF-8" in content, "start.sh does not set LC_ALL=ja_JP.UTF-8."
    assert "/home/user/daemon.log" in content, "start.sh does not redirect to /home/user/daemon.log."
    # Check for background execution
    assert "&" in content, "start.sh does not appear to run the daemon in the background."

def test_logrotate_config():
    """Verify the logrotate configuration file exists and has correct directives."""
    config_path = "/home/user/logrotate.conf"
    assert os.path.isfile(config_path), f"{config_path} does not exist."

    with open(config_path, "r") as f:
        content = f.read()

    assert "/home/user/daemon.log" in content, "logrotate.conf does not target /home/user/daemon.log."

    directives = ["daily", "rotate 3", "compress", "missingok"]
    for directive in directives:
        # Use regex to allow for possible whitespace variations
        pattern = r"\b" + directive.replace(" ", r"\s+") + r"\b"
        assert re.search(pattern, content), f"logrotate.conf is missing the '{directive}' directive."
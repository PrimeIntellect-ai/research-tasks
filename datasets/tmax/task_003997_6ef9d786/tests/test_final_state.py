# test_final_state.py
import os
import re
import subprocess
import pytest

def test_executable_compiled():
    """Check if the C daemon was compiled to the correct location and is executable."""
    exe_path = "/home/user/bin/interactive_daemon"
    assert os.path.isfile(exe_path), f"Executable not found at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"

def test_bashrc_environment():
    """Check if DAEMON_ENV=hardened is exported in .bashrc."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist"

    with open(bashrc_path, "r") as f:
        content = f.read()

    # Look for export DAEMON_ENV=hardened, allowing for quotes and whitespace
    pattern = r"export\s+DAEMON_ENV\s*=\s*['\"]?hardened['\"]?"
    assert re.search(pattern, content), f"DAEMON_ENV=hardened is not exported in {bashrc_path}"

def test_expect_script():
    """Check if the expect script exists and contains the PIN."""
    exp_path = "/home/user/bin/auto_start.exp"
    assert os.path.isfile(exp_path), f"Expect script not found at {exp_path}"

    with open(exp_path, "r") as f:
        content = f.read()

    assert "7924" in content, f"Expect script {exp_path} does not contain the required PIN '7924'"

def test_launch_script():
    """Check if the launch script exists and is executable."""
    launch_path = "/home/user/bin/launch.sh"
    assert os.path.isfile(launch_path), f"Launch script not found at {launch_path}"
    assert os.access(launch_path, os.X_OK), f"Launch script at {launch_path} is not executable"

def test_logrotate_config():
    """Check if the logrotate config is valid and contains the required directives."""
    conf_path = "/home/user/daemon_logrotate.conf"
    assert os.path.isfile(conf_path), f"Logrotate config not found at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/daemon_logs/app.log" in content, f"Logrotate config does not target /home/user/daemon_logs/app.log"

    # Test valid parsing using logrotate -d
    result = subprocess.run(["logrotate", "-d", conf_path], capture_output=True, text=True)
    assert result.returncode == 0, f"logrotate config failed validation: {result.stderr}"

def test_daemon_execution_and_logs():
    """Check if the daemon ran and wrote the expected logs."""
    log_path = "/home/user/daemon_logs/app.log"
    assert os.path.isfile(log_path), f"Log file not found at {log_path}. Did the wrapper script run?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "PIN accepted. Daemon initialized." in content, "Log file does not indicate successful PIN acceptance."
    assert "STATUS: Daemon running securely..." in content, "Log file does not indicate the daemon is running securely."
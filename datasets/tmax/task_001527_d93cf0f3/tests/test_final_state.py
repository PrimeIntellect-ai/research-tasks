# test_final_state.py
import os
import re
import subprocess
import pytest

def test_executable_compiled_and_runs():
    executable_path = "/home/user/net_monitor"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

    # Run the executable with the environment variable set
    env = os.environ.copy()
    env["TARGET_HOSTS"] = "test_host"

    try:
        result = subprocess.run([executable_path], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        assert result.returncode == 0, f"Executable returned non-zero exit code: {result.returncode}. Stderr: {result.stderr.decode()}"
    except Exception as e:
        pytest.fail(f"Failed to execute {executable_path}: {e}")

def test_bashrc_contains_export():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"File {bashrc_path} is missing."

    with open(bashrc_path, 'r') as f:
        content = f.read()

    # Look for export TARGET_HOSTS="127.0.0.1 1.1.1.1" or similar
    pattern = r"TARGET_HOSTS=[\"']?127\.0\.0\.1 1\.1\.1\.1[\"']?"
    assert re.search(pattern, content), f"Could not find the correct TARGET_HOSTS export in {bashrc_path}."

def test_logrotate_config():
    logrotate_path = "/home/user/logrotate.conf"
    assert os.path.isfile(logrotate_path), f"File {logrotate_path} is missing."

    with open(logrotate_path, 'r') as f:
        content = f.read()

    assert "/home/user/logs/net_monitor.log" in content, f"Logrotate config missing target log file path."

    # Check for required directives
    directives = ["daily", "rotate 3", "compress", "missingok"]
    for directive in directives:
        # Use regex to allow for varied whitespace
        pattern = r"\b" + directive.replace(" ", r"\s+") + r"\b"
        assert re.search(pattern, content), f"Logrotate config is missing the '{directive}' directive."
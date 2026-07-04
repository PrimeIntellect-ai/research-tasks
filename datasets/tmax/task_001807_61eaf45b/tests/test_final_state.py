# test_final_state.py

import os
import hashlib

def test_symlink_created_correctly():
    symlink_path = "/home/user/logs/current"
    target_path = "/home/user/app_data/logs"

    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."
    actual_target = os.readlink(symlink_path)
    assert actual_target == target_path, f"Symlink points to {actual_target}, expected {target_path}."

def test_wrapper_script_updated():
    wrapper_path = "/home/user/monitor/run_monitor.sh"
    assert os.path.isfile(wrapper_path), f"Wrapper script {wrapper_path} is missing."

    with open(wrapper_path, "r") as f:
        content = f.read()

    assert "TZ=UTC" in content, "Wrapper script does not contain 'TZ=UTC'."
    assert "LC_ALL=C" in content, "Wrapper script does not contain 'LC_ALL=C'."

def test_status_file_created():
    status_file = "/home/user/monitor/status.txt"
    assert os.path.isfile(status_file), f"Status file {status_file} was not created. Did you run the wrapper script?"

    with open(status_file, "r") as f:
        content = f.read().strip()

    expected_text = "HEALTHY: ALL CHECKS PASSED"
    assert content == expected_text, f"Status file content is '{content}', expected '{expected_text}'."

def test_check_health_script_unmodified():
    script_path = "/home/user/monitor/check_health.py"
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

    expected_content = """import os
import time
import sys

# Check timezone
if os.environ.get("TZ") != "UTC":
    print("FAIL: Expected TZ=UTC environment variable")
    sys.exit(1)

# Check locale
if os.environ.get("LC_ALL") != "C":
    print("FAIL: Expected LC_ALL=C environment variable")
    sys.exit(1)

# Check symlink path
log_file = "/home/user/logs/current/app.log"
if not os.path.exists(log_file):
    print(f"FAIL: Log file not found at {log_file}")
    sys.exit(1)

# If all pass, write status
with open("/home/user/monitor/status.txt", "w") as f:
    f.write("HEALTHY: ALL CHECKS PASSED\\n")
print("SUCCESS: Health check passed")
"""
    with open(script_path, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, "The check_health.py script was modified, which violates the constraints."
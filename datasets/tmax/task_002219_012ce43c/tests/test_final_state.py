# test_final_state.py

import os
import glob
import pytest

def test_old_files_deleted():
    logs_dir = "/home/user/provisioning/logs"
    old_files = glob.glob(os.path.join(logs_dir, "*.old"))
    assert len(old_files) == 0, f"Expected 0 .old files in {logs_dir}, but found {len(old_files)}: {old_files}"

def test_symlink_created():
    symlink_path = "/home/user/provisioning/active.conf"
    target_path = "/home/user/provisioning/configs/prod.conf"

    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."

    # Resolve the symlink to its absolute path
    actual_target = os.path.realpath(symlink_path)
    expected_target = os.path.realpath(target_path)

    assert actual_target == expected_target, f"Symlink points to {actual_target}, expected {expected_target}"

def test_script_exists_and_executable():
    script_path = "/home/user/provisioning/run_check.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_connectivity_log_content():
    log_path = "/home/user/provisioning/logs/connectivity.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did the script run?"

    with open(log_path, 'r') as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "SUCCESS: google.com:443",
        "SUCCESS: cloudflare-dns.com:53",
        "FAILURE: this-domain-does-not-exist.local:8080"
    ]

    # We check if the expected lines are present in the log file in the correct order
    # Since the script appends, there might be multiple runs, so we check if the last N lines match or just check if expected lines are in content.
    # The prompt specifies "Ensure the final connectivity.log file is formatted exactly as specified"
    # So we will check if the expected lines are in the content.

    for expected in expected_lines:
        assert expected in content, f"Expected line '{expected}' not found in {log_path}"

    # Check if the last 3 lines match exactly for a clean run
    assert content[-3:] == expected_lines, f"The last 3 lines of {log_path} do not match the expected output. Found: {content[-3:]}"
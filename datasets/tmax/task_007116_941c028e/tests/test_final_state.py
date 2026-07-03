# test_final_state.py

import os
import subprocess
import pytest

def test_log_file_exists_and_contains_string():
    log_path = "/home/user/logs/user_commits.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did the hook run correctly?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "Commit pushed at" in content, f"Log file {log_path} does not contain the expected string 'Commit pushed at'."

def test_symlink_exists_and_correct():
    symlink_path = "/home/user/public_logs/latest_commits.log"
    expected_target = "/home/user/logs/user_commits.log"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    target = os.readlink(symlink_path)
    assert target == expected_target, f"Symbolic link {symlink_path} points to {target}, expected {expected_target}."

def test_rotate_script_works():
    script_path = "/home/user/scripts/rotate.py"
    log_path = "/home/user/logs/user_commits.log"
    bak_path = "/home/user/logs/user_commits.log.bak"

    assert os.path.isfile(script_path), f"Rotation script {script_path} does not exist."

    # Write some dummy content to the log file to ensure we can verify it was rotated
    with open(log_path, "w") as f:
        f.write("Dummy content before rotation")

    # Remove existing backup if it exists to test cleanly
    if os.path.exists(bak_path):
        os.remove(bak_path)

    # Run the rotation script
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Rotation script failed to run: {result.stderr}"

    # Check if backup was created
    assert os.path.isfile(bak_path), f"Backup file {bak_path} was not created after running rotate.py."

    # Check if new log was created and is empty
    assert os.path.isfile(log_path), f"New log file {log_path} was not created after running rotate.py."
    assert os.path.getsize(log_path) == 0, f"New log file {log_path} is not empty after rotation."

def test_workspace_commit_successful():
    workspace_path = "/home/user/admin_workspace"

    # Check if alice.json is in the latest commit
    result = subprocess.run(
        ["git", "-C", workspace_path, "log", "-1", "--stat"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to run git log in workspace."
    assert "alice.json" in result.stdout, "alice.json was not found in the latest commit."
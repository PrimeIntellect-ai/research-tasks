# test_final_state.py

import os
import subprocess
import time
import pytest

def test_fix_hook_script_exists():
    script_path = "/home/user/fix_hook.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_hook_creation_and_execution():
    script_path = "/home/user/fix_hook.sh"

    # 1. Run the agent's script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Executing {script_path} failed with output: {result.stderr}"

    # 2. Check if hook exists and is executable
    hook_path = "/home/user/account_repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"The hook file {hook_path} was not created."
    assert os.access(hook_path, os.X_OK), f"The hook file {hook_path} is not executable."

    # 3. Trigger a push
    dummy_repo = "/tmp/dummy_repo"
    os.makedirs(dummy_repo, exist_ok=True)
    subprocess.run(["git", "init"], cwd=dummy_repo, check=True, capture_output=True)

    # Add remote if not exists
    remotes = subprocess.run(["git", "remote"], cwd=dummy_repo, capture_output=True, text=True).stdout
    if "origin" not in remotes:
        subprocess.run(["git", "remote", "add", "origin", "/home/user/account_repo.git"], cwd=dummy_repo, check=True)

    # Configure git so it doesn't complain
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=dummy_repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=dummy_repo, check=True)

    test_file = os.path.join(dummy_repo, "testfile")
    with open(test_file, "w") as f:
        f.write("test")

    subprocess.run(["git", "add", "testfile"], cwd=dummy_repo, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=dummy_repo, check=True, capture_output=True)

    # Push to trigger hook
    push_result = subprocess.run(["git", "push", "origin", "master"], cwd=dummy_repo, capture_output=True, text=True)
    assert push_result.returncode == 0, f"Git push failed: {push_result.stderr}"

    # 4. Wait a moment for the background process to finish
    time.sleep(1)

    # 5. Check if the log files exist in the correct location and contain expected text
    sync_log = "/home/user/logs/sync.log"
    hook_output_log = "/home/user/logs/hook_output.log"

    assert os.path.isfile(sync_log), f"{sync_log} was not created. The hook might not be exporting LOG_DIR correctly."
    with open(sync_log, "r") as f:
        sync_content = f.read()
    assert "Sync triggered" in sync_content, f"Expected 'Sync triggered' in {sync_log}, but got: {sync_content}"

    assert os.path.isfile(hook_output_log), f"{hook_output_log} was not created. Output redirection might be missing."
    with open(hook_output_log, "r") as f:
        hook_content = f.read()
    assert "Sync completed successfully." in hook_content, f"Expected 'Sync completed successfully.' in {hook_output_log}, but got: {hook_content}"

def test_idempotency():
    script_path = "/home/user/fix_hook.sh"

    # Run the script a second time
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Executing {script_path} a second time failed (not idempotent). Output: {result.stderr}"

    hook_path = "/home/user/account_repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"The hook file {hook_path} was removed or not created on second run."
    assert os.access(hook_path, os.X_OK), f"The hook file {hook_path} lost executable permissions on second run."
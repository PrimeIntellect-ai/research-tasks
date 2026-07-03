# test_final_state.py

import os
import stat
import subprocess
import re
import tempfile
import time
import pytest

def test_post_receive_hook_execution():
    repo_path = "/home/user/dashboard-repo.git"
    deploy_path = "/home/user/dashboards_deployed"
    reloaded_file = "/home/user/service_reloaded.txt"
    log_file = "/home/user/deploy.log"

    # Ensure the hook is executable
    hook_path = os.path.join(repo_path, "hooks", "post-receive")
    assert os.path.isfile(hook_path), "post-receive hook file is missing."
    assert os.access(hook_path, os.X_OK), "post-receive hook is not executable."

    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone the bare repo
        subprocess.run(
            ["git", "clone", repo_path, temp_dir],
            check=True,
            capture_output=True
        )

        # Create a test file, commit and push
        test_file_name = "test_dashboard_123.json"
        test_file_path = os.path.join(temp_dir, test_file_name)
        with open(test_file_path, "w") as f:
            f.write("{}")

        subprocess.run(["git", "add", test_file_name], cwd=temp_dir, check=True, capture_output=True)

        # We need to configure git user for commit if not set
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_dir, check=True, capture_output=True)

        subprocess.run(["git", "commit", "-m", "Test push"], cwd=temp_dir, check=True, capture_output=True)

        # Push to trigger the hook
        push_result = subprocess.run(["git", "push", "origin", "master"], cwd=temp_dir, capture_output=True)
        assert push_result.returncode == 0, f"Git push failed: {push_result.stderr.decode()}"

    # Give the hook a tiny moment to finish if needed
    time.sleep(0.5)

    # 1. Check if the file was deployed
    deployed_file_path = os.path.join(deploy_path, test_file_name)
    assert os.path.isfile(deployed_file_path), f"File was not deployed to {deploy_path}"

    # 2. Check permissions (750)
    dir_stat = os.stat(deploy_path)
    assert oct(dir_stat.st_mode & 0o777) == '0o750', f"Directory permissions for {deploy_path} are not 750"

    file_stat = os.stat(deployed_file_path)
    assert oct(file_stat.st_mode & 0o777) == '0o750', f"File permissions for {deployed_file_path} are not 750"

    # 3. Check if SIGHUP was sent (mock service trap triggers file creation)
    assert os.path.isfile(reloaded_file), "SIGHUP was not sent to the dashboard service (service_reloaded.txt missing)"

    # 4. Check deploy.log for correct format
    assert os.path.isfile(log_file), f"Audit log file {log_file} is missing"

    with open(log_file, "r") as f:
        log_contents = f.read().strip().split('\n')

    assert len(log_contents) > 0, "Log file is empty"

    last_log = log_contents[-1]
    log_pattern = r'^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Dashboards reloaded$'
    assert re.match(log_pattern, last_log), f"Log entry format is incorrect. Found: {last_log}"
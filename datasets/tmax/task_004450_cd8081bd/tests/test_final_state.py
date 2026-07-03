# test_final_state.py

import os
import re
import pytest

def test_deployment_restore():
    """Verify the backup was extracted and the symlink was created properly."""
    deployments_dir = "/home/user/deployments"
    app_v1 = os.path.join(deployments_dir, "app-v1")
    app_v2 = os.path.join(deployments_dir, "app-v2")
    live_link = os.path.join(deployments_dir, "live")

    assert os.path.isdir(app_v1), f"Expected extracted directory {app_v1} not found."
    assert os.path.isdir(app_v2), f"Expected extracted directory {app_v2} not found."

    assert os.path.islink(live_link), f"Expected {live_link} to be a symbolic link."
    target = os.readlink(live_link)
    # The target can be absolute or relative
    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(deployments_dir, target))
    assert target == app_v2, f"Expected {live_link} to point to {app_v2}, but points to {target}"

def test_storage_monitoring():
    """Verify that large files (>100KB) are logged correctly."""
    log_file = "/home/user/large_files.log"
    assert os.path.isfile(log_file), f"Expected log file {log_file} not found."

    # Compute truth
    deployments_dir = "/home/user/deployments"
    expected_large_files = set()
    if os.path.isdir(deployments_dir):
        for root, dirs, files in os.walk(deployments_dir):
            for file in files:
                filepath = os.path.join(root, file)
                if not os.path.islink(filepath) and os.path.getsize(filepath) > 100 * 1024:
                    expected_large_files.add(filepath)

    with open(log_file, 'r') as f:
        actual_lines = {line.strip() for line in f if line.strip()}

    assert actual_lines == expected_large_files, f"Expected {log_file} to contain exactly {expected_large_files}, but got {actual_lines}"

def test_user_access_administration():
    """Verify the proxy_users.txt file is created with correct basic auth format."""
    auth_file = "/home/user/proxy_users.txt"
    assert os.path.isfile(auth_file), f"Expected basic auth file {auth_file} not found."

    with open(auth_file, 'r') as f:
        content = f.read().strip()

    assert "backup_admin:" in content, f"Expected user 'backup_admin' in {auth_file}."

    # Check for MD5 apr1 hash
    match = re.search(r'^backup_admin:\$apr1\$[a-zA-Z0-9./]+\$[a-zA-Z0-9./]+', content, re.MULTILINE)
    assert match is not None, f"Expected 'backup_admin' to have an Apache MD5 ($apr1$) hashed password in {auth_file}."

def test_proxy_setup():
    """Verify the start_proxy.sh script exists, is executable, and contains necessary references."""
    script_file = "/home/user/start_proxy.sh"
    assert os.path.isfile(script_file), f"Expected script file {script_file} not found."

    assert os.access(script_file, os.X_OK), f"Expected {script_file} to be executable."

    with open(script_file, 'r') as f:
        content = f.read()

    assert "8080" in content, f"Expected reference to port 8080 in {script_file}."
    assert "9090" in content, f"Expected reference to port 9090 in {script_file}."
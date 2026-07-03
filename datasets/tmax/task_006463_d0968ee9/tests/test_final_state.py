# test_final_state.py

import os
import subprocess
import pytest

def test_latest_deployment_fstab():
    """Verify that the latest_deployment.fstab file is correctly sorted."""
    fstab_path = '/home/user/latest_deployment.fstab'
    assert os.path.exists(fstab_path), f"File not found: {fstab_path}"

    with open(fstab_path, 'r') as f:
        lines = f.read().strip().split('\n')

    actual_fstab = [' '.join(line.split()) for line in lines if line.strip()]

    expected_fstab = [
        "/dev/vda /mnt/data ext4 defaults 0 2",
        "/dev/vdb /mnt/data/logs ext4 defaults 0 2",
        "/dev/vdc /mnt/data/logs/archive ext4 defaults 0 2"
    ]

    assert actual_fstab == expected_fstab, f"Fstab content is incorrect.\nExpected: {expected_fstab}\nGot: {actual_fstab}"

def test_git_repo_and_deploy_status():
    """Verify the git repository and the deployment status log."""
    repo_path = '/home/user/iot-repo.git'
    assert os.path.isdir(repo_path), f"Git repo not found: {repo_path}"

    # Get latest commit hash
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        latest_commit = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to get latest commit from {repo_path}: {e.stderr}")

    log_path = '/home/user/deploy_status.log'
    assert os.path.exists(log_path), f"Log file not found: {log_path}"

    expected_log_entry = f"DEPLOY_SUCCESS: {latest_commit}"
    with open(log_path, 'r') as f:
        log_content = f.read()

    assert expected_log_entry in log_content, f"Log file does not contain expected entry: '{expected_log_entry}'"
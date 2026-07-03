# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/operator_sync.py"
RAW_MANIFESTS_DIR = "/home/user/raw_manifests"
STRUCTURED_MANIFESTS_DIR = "/home/user/structured_manifests"
LOG_FILE = "/home/user/operator_status.log"
FSTAB_FILE = "/home/user/k8s_backup_fstab"

def test_script_exists():
    """Check if the operator_sync.py script exists."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_symlinks_created():
    """Check if the directory structure and symlinks are created correctly."""
    deployment_link = os.path.join(STRUCTURED_MANIFESTS_DIR, "Deployment", "app-deployment.yaml")
    service_link = os.path.join(STRUCTURED_MANIFESTS_DIR, "Service", "app-service.yaml")

    assert os.path.islink(deployment_link), f"{deployment_link} is not a symlink."
    assert os.readlink(deployment_link) == os.path.join(RAW_MANIFESTS_DIR, "app-deployment.yaml"), \
        f"{deployment_link} does not point to the correct raw manifest."

    assert os.path.islink(service_link), f"{service_link} is not a symlink."
    assert os.readlink(service_link) == os.path.join(RAW_MANIFESTS_DIR, "app-service.yaml"), \
        f"{service_link} does not point to the correct raw manifest."

def test_log_file_content():
    """Check if the log file contains the correct quota status."""
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."

    total_size = sum(
        os.path.getsize(os.path.join(RAW_MANIFESTS_DIR, f))
        for f in os.listdir(RAW_MANIFESTS_DIR)
        if os.path.isfile(os.path.join(RAW_MANIFESTS_DIR, f))
    )

    expected_status = "QUOTA EXCEEDED" if total_size > 1024 else "QUOTA OK"

    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, f"Log file {LOG_FILE} is empty."
    assert expected_status in lines[-1], f"Log file {LOG_FILE} does not contain the expected status '{expected_status}' in the last line."

def test_cron_job_configured():
    """Check if the cron job is configured correctly."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to retrieve crontab. Is it configured?")

    assert "*/5 * * * *" in crontab_content, "Cron job is not scheduled to run every 5 minutes."
    assert "operator_sync.py" in crontab_content, "Cron job does not execute operator_sync.py."

def test_fstab_file_content():
    """Check if the mock fstab file has the correct content."""
    assert os.path.isfile(FSTAB_FILE), f"File {FSTAB_FILE} does not exist."

    with open(FSTAB_FILE, 'r') as f:
        content = f.read().strip()

    expected_line = "/dev/sdc1 /home/user/structured_manifests ext4 defaults,usrquota 0 2"
    assert content == expected_line, f"Content of {FSTAB_FILE} is incorrect. Expected: '{expected_line}', Got: '{content}'"
# test_final_state.py

import os
import subprocess
import re
import pytest

def test_backups_exist():
    """Check if the backup files were created correctly."""
    v1_path = "/home/user/backups/app_v1.txt"
    v2_path = "/home/user/backups/app_v2.txt"

    assert os.path.isfile(v1_path), f"{v1_path} does not exist."
    with open(v1_path, "r") as f:
        assert f.read().strip() == "version 1 backup", f"Incorrect content in {v1_path}"

    assert os.path.isfile(v2_path), f"{v2_path} does not exist."
    with open(v2_path, "r") as f:
        assert f.read().strip() == "version 2 backup", f"Incorrect content in {v2_path}"

def test_rust_script_and_binary_exist():
    """Check if the Rust script and compiled binary exist."""
    rs_path = "/home/user/deploy_restore.rs"
    bin_path = "/home/user/deploy_restore"

    assert os.path.isfile(rs_path), f"{rs_path} does not exist."
    assert os.path.isfile(bin_path), f"{bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable."

def test_active_files_state():
    """Check the state of the files in the active directory after running the script twice."""
    app_path = "/home/user/active/app.txt"
    log_path = "/home/user/active/deploy.log"
    log_old_path = "/home/user/active/deploy.log.old"

    assert os.path.isfile(app_path), f"{app_path} does not exist."
    with open(app_path, "r") as f:
        assert f.read().strip() == "version 2 backup", f"Incorrect content in {app_path}"

    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, "r") as f:
        assert f.read().strip() == "Deployed v2", f"Incorrect content in {log_path}"

    assert os.path.isfile(log_old_path), f"{log_old_path} does not exist."
    with open(log_old_path, "r") as f:
        assert f.read().strip() == "Deployed v1", f"Incorrect content in {log_old_path}"

def test_cron_configuration():
    """Check if the cron job was installed correctly."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it installed for the current user?")

    # Allow for minor whitespace variations
    pattern = r"0\s+3\s+\*\s+\*\s+\*\s+/home/user/deploy_restore\s+3"
    assert re.search(pattern, crontab_output), f"Crontab does not contain the expected schedule. Got:\n{crontab_output}"
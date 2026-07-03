# test_final_state.py

import os
import stat
import subprocess
import pytest
import shutil

SCRIPT_PATH = "/home/user/generate_metric.py"
DATA_DIR = "/home/user/data_dir"
LOG_FILE = "/home/user/dashboard.log"
REPO_DIR = "/home/user/dash_repo"
HOOK_PATH = os.path.join(REPO_DIR, ".git/hooks/pre-commit")

def get_total_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

def test_generate_metric_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    # It might be executed via `python3 script.py` in the hook, but let's check if it's there.

def test_generate_metric_behavior():
    # Clean up log if exists
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # Ensure data_dir has less than 5000 bytes
    # Create a temp file to control size
    test_file = os.path.join(DATA_DIR, "test_size.bin")
    if os.path.exists(test_file):
        os.remove(test_file)

    current_size = get_total_size(DATA_DIR)
    if current_size > 4000:
        # Clear out data dir for testing
        for f in os.listdir(DATA_DIR):
            os.remove(os.path.join(DATA_DIR, f))
        current_size = 0

    # Add 2000 bytes
    with open(test_file, "wb") as f:
        f.write(b"0" * 2000)

    expected_size = get_total_size(DATA_DIR)

    # Run script
    result = subprocess.run(["python3", SCRIPT_PATH], capture_output=True)
    assert result.returncode == 0, f"Script exited with {result.returncode} but size is {expected_size} (<= 5000)."

    # Check log
    assert os.path.isfile(LOG_FILE), "Log file was not created."
    with open(LOG_FILE, "r") as f:
        lines = f.read().strip().split('\n')
    assert f"METRIC: {expected_size}" in lines[-1], f"Expected 'METRIC: {expected_size}' in log, got '{lines[-1]}'."

    # Increase size to > 5000
    with open(test_file, "ab") as f:
        f.write(b"0" * 4000)

    expected_size_large = get_total_size(DATA_DIR)
    result = subprocess.run(["python3", SCRIPT_PATH], capture_output=True)
    assert result.returncode == 1, f"Script exited with {result.returncode} but size is {expected_size_large} (> 5000)."

    with open(LOG_FILE, "r") as f:
        lines = f.read().strip().split('\n')
    assert f"METRIC: {expected_size_large}" in lines[-1], f"Expected 'METRIC: {expected_size_large}' in log, got '{lines[-1]}'."

    # Cleanup
    os.remove(test_file)

def test_git_pre_commit_hook():
    assert os.path.isfile(HOOK_PATH), f"Git hook not found at {HOOK_PATH}."
    assert os.access(HOOK_PATH, os.X_OK), f"Git hook at {HOOK_PATH} is not executable."

    # Ensure size is small
    test_file = os.path.join(DATA_DIR, "test_size.bin")
    if os.path.exists(test_file):
        os.remove(test_file)
    with open(test_file, "wb") as f:
        f.write(b"0" * 1000)

    # Try committing
    test_commit_file = os.path.join(REPO_DIR, "test_commit.txt")
    with open(test_commit_file, "w") as f:
        f.write("test")

    subprocess.run(["git", "add", "test_commit.txt"], cwd=REPO_DIR, check=True)
    result = subprocess.run(["git", "commit", "-m", "Test commit"], cwd=REPO_DIR, capture_output=True)
    assert result.returncode == 0, "Git commit failed when data dir size was <= 5000 bytes."

    # Make size large
    with open(test_file, "ab") as f:
        f.write(b"0" * 5000)

    with open(test_commit_file, "w") as f:
        f.write("test2")

    subprocess.run(["git", "add", "test_commit.txt"], cwd=REPO_DIR, check=True)
    result = subprocess.run(["git", "commit", "-m", "Test commit 2"], cwd=REPO_DIR, capture_output=True)
    assert result.returncode != 0, "Git commit succeeded when data dir size was > 5000 bytes. Pre-commit hook failed to block."

    # Cleanup
    os.remove(test_file)

def test_cron_job():
    # The cron job should be scheduled for the user. We can check crontab -l for both root and user
    try:
        result_user = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)
        crontab_out = result_user.stdout
    except Exception:
        crontab_out = ""

    if "generate_metric.py" not in crontab_out:
        # Fallback to current user
        result_current = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        crontab_out = result_current.stdout

    assert "generate_metric.py" in crontab_out, "Cron job for generate_metric.py not found in crontab."

    # Check for */5
    valid_cron = False
    for line in crontab_out.splitlines():
        if "generate_metric.py" in line and not line.strip().startswith("#"):
            parts = line.split()
            if len(parts) >= 5:
                # Check if it runs every 5 minutes. Standard is */5 * * * *
                if parts[0] == "*/5" and parts[1] == "*" and parts[2] == "*" and parts[3] == "*" and parts[4] == "*":
                    valid_cron = True
                    break
    assert valid_cron, "Cron job is not correctly scheduled for exactly every 5 minutes using standard syntax (*/5 * * * *)."
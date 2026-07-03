# test_final_state.py

import os
import subprocess
import time
import shutil
import re

def test_disk_monitor_script():
    script_path = "/home/user/disk_monitor.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    log_path = "/home/user/monitor_alert.log"
    data_dir = "/home/user/migration_data"
    backup_dir = "/home/user/migration_data_backup"

    # Ensure the directory has > 1000000 bytes (should be ~2MB from setup)
    # Run the script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {script_path} failed with error:\n{result.stderr}"

    assert os.path.isfile(log_path), f"Log file {log_path} was not created."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "QUOTA_EXCEEDED", f"Expected 'QUOTA_EXCEEDED', got '{content}'"

    # Test the <= 1000000 bytes condition
    # Move data out temporarily
    if os.path.exists(backup_dir):
        shutil.rmtree(backup_dir)
    shutil.move(data_dir, backup_dir)
    os.makedirs(data_dir)

    try:
        result = subprocess.run(["bash", script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Running {script_path} failed on empty dir."

        with open(log_path, "r") as f:
            content = f.read().strip()
        assert content == "OK", f"Expected 'OK' for small directory, got '{content}'"
    finally:
        # Restore data
        shutil.rmtree(data_dir)
        shutil.move(backup_dir, data_dir)

def test_crontab_scheduled():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."

    # Normalize spaces
    crontab_lines = result.stdout.strip().split('\n')
    found = False
    for line in crontab_lines:
        if line.startswith('#'):
            continue
        # Replace multiple spaces/tabs with single space
        normalized = re.sub(r'\s+', ' ', line.strip())
        if normalized == "* * * * * /home/user/disk_monitor.sh":
            found = True
            break

    assert found, "Could not find '* * * * * /home/user/disk_monitor.sh' in crontab."

def test_start_pipeline_script():
    script_path = "/home/user/start_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Clean up any previous runs
    subprocess.run(["pkill", "-f", "python3 -m http.server 8888"], capture_output=True)
    status_log = "/home/user/pipeline_status.log"
    pids_file = "/home/user/pipeline.pids"
    if os.path.exists(status_log):
        os.remove(status_log)
    if os.path.exists(pids_file):
        os.remove(pids_file)

    # Run the start script
    try:
        result = subprocess.run(["bash", script_path], capture_output=True, text=True, timeout=15)
        assert result.returncode == 0, f"{script_path} failed to execute."
    except subprocess.TimeoutExpired:
        assert False, f"{script_path} timed out. It should run processes in the background and exit."

    # Wait a bit for processor to write to log
    time.sleep(5)

    # Check PIDs file
    assert os.path.isfile(pids_file), f"{pids_file} was not created."
    with open(pids_file, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2, f"Expected exactly 2 lines in {pids_file}, found {len(lines)}."
    assert lines[0].isdigit(), f"First line of {pids_file} is not a valid PID: {lines[0]}"
    assert lines[1].isdigit(), f"Second line of {pids_file} is not a valid PID: {lines[1]}"

    # Check status log
    assert os.path.isfile(status_log), f"{status_log} was not created. The processor might not have run or failed."
    with open(status_log, "r") as f:
        status = f.read().strip()

    assert "SUCCESS" in status, f"Expected 'SUCCESS' in {status_log}, got: '{status}'. Port 8888 was likely not ready when processor started."

    # Cleanup
    subprocess.run(["kill", lines[0], lines[1]], capture_output=True)
    subprocess.run(["pkill", "-f", "python3 -m http.server 8888"], capture_output=True)
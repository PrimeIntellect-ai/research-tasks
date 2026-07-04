# test_final_state.py

import os
import glob
import time
import subprocess
import pytest

def test_auto_restore_expect_script():
    expect_script = "/home/user/auto_restore.exp"
    assert os.path.exists(expect_script), f"Expect script not found at {expect_script}"

    try:
        res = subprocess.run(["expect", expect_script], capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail("Expect script timed out after 5 seconds.")

    assert res.returncode == 0, f"Expect script failed with return code {res.returncode}. Output: {res.stdout}\nError: {res.stderr}"
    assert "Restore successful" in res.stdout, f"Restore CLI did not succeed. Output: {res.stdout}"

def test_backup_service_performance_and_correctness():
    raw_dir = "/home/user/data/raw"
    backup_dir = "/home/user/data/backup"

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)

    # Clean up directories first
    for f in glob.glob(os.path.join(raw_dir, "*")):
        os.remove(f)
    for f in glob.glob(os.path.join(backup_dir, "*")):
        os.remove(f)

    # Generate 5000 files
    for i in range(5000):
        with open(os.path.join(raw_dir, f"file_{i}.txt"), "w") as f:
            f.write("DUMMY LOG DATA" * 10)

    # Check that backup script exists
    backup_script = "/home/user/backup_service.py"
    assert os.path.exists(backup_script), f"Backup script not found at {backup_script}"

    # Run the backup service
    start_time = time.time()
    res = subprocess.run(["python3", backup_script], capture_output=True, text=True)
    duration = time.time() - start_time

    assert res.returncode == 0, f"Backup service failed with return code {res.returncode}. Error: {res.stderr}"

    raw_files = glob.glob(os.path.join(raw_dir, "*"))
    backup_files = glob.glob(os.path.join(backup_dir, "*.gz"))

    assert len(raw_files) == 0, f"Raw directory not empty, found {len(raw_files)} files."
    assert len(backup_files) == 5000, f"Backup directory missing files, found {len(backup_files)} files."

    assert duration <= 2.0, f"Performance threshold failed. Time taken: {duration:.2f}s (Threshold: 2.0s)"
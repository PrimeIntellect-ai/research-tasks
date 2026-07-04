# test_final_state.py

import os
import subprocess
import time
import glob
import pytest

def test_deployment_structure():
    v1_dir = "/home/user/deployment/releases/v1.0.0"
    v2_dir = "/home/user/deployment/releases/v2.0.0"
    current_link = "/home/user/deployment/current"

    assert os.path.isdir(v1_dir), f"Directory missing: {v1_dir}"
    assert os.path.isdir(v2_dir), f"Directory missing: {v2_dir}"
    assert os.path.islink(current_link), f"Not a symlink: {current_link}"

    target = os.readlink(current_link)
    # Target could be absolute or relative
    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(os.path.dirname(current_link), target))

    assert target == v2_dir, f"Symlink {current_link} points to {target}, expected {v2_dir}"

def test_filter_script_corpus():
    script_path = "/home/user/deployment/current/filter.py"
    assert os.path.isfile(script_path), f"Filter script missing: {script_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run(["python3", script_path, cf], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run(["python3", script_path, ef], capture_output=True)
        if res.returncode == 0:
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_log_rotation():
    rotate_script = "/home/user/deployment/current/rotate.sh"
    assert os.path.isfile(rotate_script), f"Rotate script missing: {rotate_script}"
    assert os.access(rotate_script, os.X_OK), f"Rotate script is not executable: {rotate_script}"

    logs_dir = "/home/user/logs"
    access_log = os.path.join(logs_dir, "access.log")

    # Ensure logs dir exists
    os.makedirs(logs_dir, exist_ok=True)

    # Run the script 5 times
    for i in range(5):
        with open(access_log, "w") as f:
            f.write(f"log entry {i}\n")

        res = subprocess.run(["bash", rotate_script], capture_output=True)
        assert res.returncode == 0, f"Rotate script failed on run {i+1} with error: {res.stderr.decode()}"

        # slight delay to ensure different timestamps if script uses seconds
        time.sleep(1.1)

    assert os.path.isfile(access_log), f"New access.log was not created"
    assert os.path.getsize(access_log) == 0, f"New access.log is not empty"

    archived_logs = glob.glob(os.path.join(logs_dir, "access.log.*"))
    assert len(archived_logs) <= 3, f"Expected at most 3 archived logs, found {len(archived_logs)}"
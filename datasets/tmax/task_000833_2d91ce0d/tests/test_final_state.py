# test_final_state.py

import os
import subprocess
import glob
import pytest

CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def get_script_path():
    py_script = "/home/user/filter_data.py"
    sh_script = "/home/user/filter_data.sh"

    if os.path.exists(py_script):
        return py_script
    elif os.path.exists(sh_script):
        return sh_script
    else:
        return None

def test_script_exists():
    script_path = get_script_path()
    assert script_path is not None, "Could not find /home/user/filter_data.py or /home/user/filter_data.sh"
    assert os.path.isfile(script_path), f"{script_path} is not a file"

def test_adversarial_corpus():
    script_path = get_script_path()
    if not script_path:
        pytest.fail("Script not found.")

    is_python = script_path.endswith('.py')

    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.csv"))

    assert len(clean_files) > 0, f"No clean CSV files found in {CLEAN_DIR}"
    assert len(evil_files) > 0, f"No evil CSV files found in {EVIL_DIR}"

    clean_failures = []
    evil_failures = []

    for clean_file in clean_files:
        cmd = ["python3", script_path, clean_file] if is_python else ["bash", script_path, clean_file]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(clean_file))

    for evil_file in evil_files:
        cmd = ["python3", script_path, evil_file] if is_python else ["bash", script_path, evil_file]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(evil_file))

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))
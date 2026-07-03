# test_final_state.py

import os
import subprocess
import pytest
import glob

def test_detector_script_exists_and_executable():
    script_path = "/home/user/detector.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_adversarial_corpus():
    script_path = "/home/user/detector.sh"

    clean_dir = "/app/clean"
    evil_dir = "/app/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    rejected_clean = []
    bypassed_evil = []

    for clean_file in clean_files:
        result = subprocess.run([script_path, clean_file], capture_output=True)
        if result.returncode != 0:
            rejected_clean.append(os.path.basename(clean_file))

    for evil_file in evil_files:
        result = subprocess.run([script_path, evil_file], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(evil_file))

    error_messages = []
    if rejected_clean:
        error_messages.append(f"{len(rejected_clean)} of {len(clean_files)} clean files rejected: {', '.join(rejected_clean)}")
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed: {', '.join(bypassed_evil)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))
# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_detect_script_exists():
    script_path = "/home/user/detect.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_clean_corpus():
    script_path = "/home/user/detect.sh"
    clean_dir = "/app/corpus/clean/"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(clean_files) > 0, f"No CSV files found in {clean_dir}."

    failed_files = []
    for f in clean_files:
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected (expected exit code 0). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    script_path = "/home/user/detect.sh"
    evil_dir = "/app/corpus/evil/"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(evil_files) > 0, f"No CSV files found in {evil_dir}."

    failed_files = []
    for f in evil_files:
        result = subprocess.run([script_path, f], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(f))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}")
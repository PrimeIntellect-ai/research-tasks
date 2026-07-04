# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_evaluate_run_script_exists_and_executable():
    script_path = "/home/user/evaluate_run.sh"
    assert os.path.exists(script_path), f"Script missing: {script_path}"
    assert os.path.isfile(script_path), f"Path is not a file: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_adversarial_corpus():
    script_path = "/home/user/evaluate_run.sh"
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(evil_files) > 0, "No evil files found to test."
    assert len(clean_files) > 0, "No clean files found to test."

    evil_bypassed = []
    for f in evil_files:
        result = subprocess.run(["bash", script_path, f], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        result = subprocess.run(["bash", script_path, f], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))
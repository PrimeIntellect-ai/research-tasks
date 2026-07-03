# test_final_state.py

import os
import subprocess
import pytest

def test_classifier_binary_exists():
    binary_path = "/home/user/classifier"
    assert os.path.isfile(binary_path), f"Classifier binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Classifier binary at {binary_path} is not executable"

def test_classifier_behavior():
    binary_path = "/home/user/classifier"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    assert len(clean_files) > 0, "No clean files found to test."
    assert len(evil_files) > 0, "No evil files found to test."

    clean_failures = []
    for cf in clean_files:
        res = subprocess.run([binary_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failures.append(os.path.basename(cf))

    evil_failures = []
    for ef in evil_files:
        res = subprocess.run([binary_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failures.append(os.path.basename(ef))

    err_msgs = []
    if evil_failures:
        err_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        err_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if err_msgs:
        pytest.fail(" | ".join(err_msgs))
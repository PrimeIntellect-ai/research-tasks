# test_final_state.py

import os
import subprocess
import pytest

def test_recovered_key():
    key_path = "/home/user/recovered_key.txt"
    assert os.path.exists(key_path), f"Recovered key file missing at {key_path}"

    with open(key_path, "r") as f:
        key = f.read().strip()

    expected_key = "4a2b9c118f7e6d5c2233445566778899"
    assert key == expected_key, f"Recovered key is incorrect. Expected {expected_key}, got {key}"

def test_classifier_exists():
    script_path = "/home/user/log_classifier.py"
    assert os.path.exists(script_path), f"Classifier script missing at {script_path}"

def test_classifier_accuracy():
    script_path = "/home/user/log_classifier.py"
    assert os.path.exists(script_path), "Classifier script is missing."

    evil_dir = "/test_data/unencrypted_corpora/evil/"
    clean_dir = "/test_data/unencrypted_corpora/clean/"

    assert os.path.exists(evil_dir), "Hidden evil corpus missing."
    assert os.path.exists(clean_dir), "Hidden clean corpus missing."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    bypassed_evil = []
    modified_clean = []

    for ef in evil_files:
        result = subprocess.run(["python3", script_path, ef], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(ef))

    for cf in clean_files:
        result = subprocess.run(["python3", script_path, cf], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(cf))

    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if error_messages:
        pytest.fail("Classifier failed: " + " | ".join(error_messages))
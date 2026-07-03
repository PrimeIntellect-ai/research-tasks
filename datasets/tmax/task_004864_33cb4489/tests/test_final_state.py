# test_final_state.py

import os
import subprocess
import pytest

def test_mock_ids_binary_exists():
    """Ensure the mock_ids binary has been compiled and is executable."""
    binary_path = "/home/user/mock_ids"
    assert os.path.exists(binary_path), f"The binary {binary_path} does not exist."
    assert os.path.isfile(binary_path), f"Expected {binary_path} to be a file."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_adversarial_corpus():
    """Test the mock_ids binary against the hidden adversarial corpus."""
    binary_path = "/home/user/mock_ids"
    evil_dir = "/app/hidden_eval/evil"
    clean_dir = "/app/hidden_eval/clean"

    evil_bypassed = []
    clean_modified = []

    total_evil = 0
    total_clean = 0

    # Evaluate Evil Corpus
    if os.path.exists(evil_dir):
        for f in os.listdir(evil_dir):
            file_path = os.path.join(evil_dir, f)
            if os.path.isfile(file_path):
                total_evil += 1
                result = subprocess.run([binary_path, file_path], capture_output=True)
                if result.returncode != 1:
                    evil_bypassed.append(f)

    # Evaluate Clean Corpus
    if os.path.exists(clean_dir):
        for f in os.listdir(clean_dir):
            file_path = os.path.join(clean_dir, f)
            if os.path.isfile(file_path):
                total_clean += 1
                result = subprocess.run([binary_path, file_path], capture_output=True)
                if result.returncode != 0:
                    clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {total_evil} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {total_clean} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))
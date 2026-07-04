# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_classifier_clean_corpus():
    """Test that the classifier accepts all clean files (exit code 0)."""
    script_path = "/home/user/classifier.py"
    assert os.path.isfile(script_path), f"Classifier script missing: {script_path}"

    clean_dir = "/app/data/hidden_clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    assert len(clean_files) > 0, f"No clean files found in {clean_dir}"

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0): {failed_files}")

def test_classifier_evil_corpus():
    """Test that the classifier rejects all evil files (exit code 1)."""
    script_path = "/home/user/classifier.py"
    assert os.path.isfile(script_path), f"Classifier script missing: {script_path}"

    evil_dir = "/app/data/hidden_evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    assert len(evil_files) > 0, f"No evil files found in {evil_dir}"

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed detection (exit code != 1): {failed_files}")
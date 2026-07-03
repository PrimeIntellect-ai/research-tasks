# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_librk4_compiled():
    """Test that the C library was compiled into a shared object."""
    so_path = "/app/src/librk4.so"
    assert os.path.isfile(so_path), f"Shared library not found at {so_path}. Did you compile rk4_core.c?"

def test_detector_script_exists():
    """Test that the detector script exists."""
    script_path = "/home/user/detector.py"
    assert os.path.isfile(script_path), f"Detector script not found at {script_path}"

def test_detector_adversarial_corpus():
    """Test the detector script against the clean and evil corpora."""
    script_path = "/home/user/detector.py"
    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*.npy"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.npy"))

    assert len(clean_files) > 0, "No clean corpus files found to test."
    assert len(evil_files) > 0, "No evil corpus files found to test."

    clean_failed = []
    for filepath in clean_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(filepath))

    evil_failed = []
    for filepath in evil_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(filepath))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))
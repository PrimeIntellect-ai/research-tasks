# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_detector_script_exists():
    """Verify that the detector script exists."""
    script_path = "/home/user/detector.py"
    assert os.path.exists(script_path), f"Detector script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_detector_accuracy():
    """Verify that the detector correctly classifies all clean and evil files."""
    script_path = "/home/user/detector.py"
    assert os.path.exists(script_path), "Detector script missing."

    clean_dir = "/app/data/clean"
    evil_dir = "/app/data/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, "No clean files found."
    assert len(evil_files) > 0, "No evil files found."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run(["python3", script_path, f], capture_output=True)
        if result.returncode != 1:
            evil_failed.append(os.path.basename(f))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected instead of accepted): {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted instead of rejected): {', '.join(evil_failed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))

def test_libdist_installed():
    """Verify that the libdist module is installed and importable."""
    try:
        result = subprocess.run(["python3", "-c", "import libdist"], capture_output=True, text=True)
        assert result.returncode == 0, "libdist module is not installed or failed to import."
    except Exception as e:
        pytest.fail(f"Failed to check libdist installation: {e}")
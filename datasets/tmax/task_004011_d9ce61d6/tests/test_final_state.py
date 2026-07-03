# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_detector_executable_exists():
    executable = "/home/user/detector"
    assert os.path.isfile(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_evil_corpus_rejected():
    executable = "/home/user/detector"
    if not os.path.isfile(executable) or not os.access(executable, os.X_OK):
        pytest.fail("Detector executable is missing or not executable.")

    evil_dir = "/app/corpora/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(evil_files) > 0, "No evil corpus files found."

    bypassed = []
    for f in evil_files:
        try:
            result = subprocess.run([executable, f], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "REJECT":
                bypassed.append(os.path.basename(f))
        except Exception as e:
            bypassed.append(f"{os.path.basename(f)} (error: {e})")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_clean_corpus_accepted():
    executable = "/home/user/detector"
    if not os.path.isfile(executable) or not os.access(executable, os.X_OK):
        pytest.fail("Detector executable is missing or not executable.")

    clean_dir = "/app/corpora/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))

    assert len(clean_files) > 0, "No clean corpus files found."

    modified = []
    for f in clean_files:
        try:
            result = subprocess.run([executable, f], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "ACCEPT":
                modified.append(os.path.basename(f))
        except Exception as e:
            modified.append(f"{os.path.basename(f)} (error: {e})")

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified. Offending files: {', '.join(modified)}")
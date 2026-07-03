# test_final_state.py

import os
import glob
import subprocess
import pytest

def test_papermill_installed_and_fixed():
    """Check that papermill is installed and the CLI works (typo fixed)."""
    try:
        result = subprocess.run(
            ["papermill", "--help"],
            capture_output=True,
            text=True,
            check=True
        )
        assert "Usage:" in result.stdout or "papermill" in result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"papermill is not properly installed or the typo is not fixed. Running papermill --help failed with: {e.stderr}")
    except FileNotFoundError:
        pytest.fail("papermill command not found. It was not installed correctly.")

def test_scripts_exist_and_executable():
    """Check that the required bash scripts exist and are executable."""
    detector = "/home/user/detect_bad_spectrum.sh"
    orchestrator = "/home/user/orchestrate.sh"

    assert os.path.isfile(detector), f"Script {detector} does not exist."
    assert os.access(detector, os.X_OK), f"Script {detector} is not executable."

    assert os.path.isfile(orchestrator), f"Script {orchestrator} does not exist."
    assert os.access(orchestrator, os.X_OK), f"Script {orchestrator} is not executable."

def test_adversarial_corpus_detector():
    """Test detect_bad_spectrum.sh against the clean and evil corpora."""
    detector = "/home/user/detect_bad_spectrum.sh"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([detector, f], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 0 or output != "VALID":
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([detector, f], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 1 or output != "INVALID":
            evil_failures.append(os.path.basename(f))

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failures)}")

    if error_msgs:
        pytest.fail("Corpus verification failed:\n" + "\n".join(error_msgs))
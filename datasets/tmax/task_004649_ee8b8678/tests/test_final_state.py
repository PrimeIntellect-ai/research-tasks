# test_final_state.py

import os
import subprocess
import pytest

DETECT_SCRIPT = "/home/user/detect.sh"
EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"

def test_detect_script_exists_and_executable():
    """Ensure the detect.sh script exists and is executable."""
    assert os.path.isfile(DETECT_SCRIPT), f"The classifier script {DETECT_SCRIPT} is missing."
    assert os.access(DETECT_SCRIPT, os.X_OK), f"The classifier script {DETECT_SCRIPT} is not executable."

def test_adversarial_corpus():
    """Test the classifier against the clean and evil corpora."""

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".csv")]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".csv")]

    assert len(evil_files) > 0, f"No CSV files found in {EVIL_CORPUS_DIR}"
    assert len(clean_files) > 0, f"No CSV files found in {CLEAN_CORPUS_DIR}"

    bypassed_evil = []
    for evil_file in evil_files:
        result = subprocess.run([DETECT_SCRIPT, evil_file], capture_output=True)
        if result.returncode != 1:
            bypassed_evil.append(os.path.basename(evil_file))

    modified_clean = []
    for clean_file in clean_files:
        result = subprocess.run([DETECT_SCRIPT, clean_file], capture_output=True)
        if result.returncode != 0:
            modified_clean.append(os.path.basename(clean_file))

    error_messages = []
    if bypassed_evil:
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(modified_clean)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))

def test_libsh_data_fixed():
    """Ensure the vendored package is fixed and operational."""
    bin_script = "/app/libsh-data-1.2.0/bin/sh-hash-row"
    assert os.path.isfile(bin_script), f"Missing {bin_script}"

    # Run it with a sample input to see if it works
    result = subprocess.run([bin_script, "sensorA,100"], capture_output=True, text=True)
    assert result.returncode == 0, f"sh-hash-row failed to execute. It might not be fixed correctly. Stderr: {result.stderr}"
    assert len(result.stdout.strip()) > 0, "sh-hash-row did not output a hash."
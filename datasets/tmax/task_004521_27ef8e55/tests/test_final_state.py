# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/detect_divergence.sh"
CLEAN_DIR = "/app/data/clean"
EVIL_DIR = "/app/data/evil"

def test_script_exists_and_executable():
    """Check that the detect_divergence.sh script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    """Test the script against the clean and evil corpora."""
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.wav"))
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.wav"))

    assert len(clean_files) > 0, "No clean files found for testing."
    assert len(evil_files) > 0, "No evil files found for testing."

    clean_failed = []
    for cf in clean_files:
        try:
            result = subprocess.run([SCRIPT_PATH, cf], capture_output=True, text=True, timeout=10)
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_failed.append((os.path.basename(cf), output))
        except Exception as e:
            clean_failed.append((os.path.basename(cf), str(e)))

    evil_failed = []
    for ef in evil_files:
        try:
            result = subprocess.run([SCRIPT_PATH, ef], capture_output=True, text=True, timeout=10)
            output = result.stdout.strip()
            if output != "EVIL":
                evil_failed.append((os.path.basename(ef), output))
        except Exception as e:
            evil_failed.append((os.path.basename(ef), str(e)))

    error_messages = []
    if clean_failed:
        failed_names = [name for name, _ in clean_failed]
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (incorrectly classified). Offending files: {', '.join(failed_names)}")

    if evil_failed:
        failed_names = [name for name, _ in evil_failed]
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (incorrectly classified). Offending files: {', '.join(failed_names)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))
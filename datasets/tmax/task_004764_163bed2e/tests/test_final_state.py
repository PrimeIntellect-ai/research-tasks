# test_final_state.py

import os
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/sanitizer.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert len(clean_files) > 0, f"No clean CSV files found in {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No evil CSV files found in {EVIL_CORPUS_DIR}"

    clean_failed = []
    evil_failed = []

    for clean_file in clean_files:
        try:
            result = subprocess.run([SCRIPT_PATH, clean_file], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "ACCEPT":
                clean_failed.append((os.path.basename(clean_file), output))
        except Exception as e:
            clean_failed.append((os.path.basename(clean_file), str(e)))

    for evil_file in evil_files:
        try:
            result = subprocess.run([SCRIPT_PATH, evil_file], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "REJECT":
                evil_failed.append((os.path.basename(evil_file), output))
        except Exception as e:
            evil_failed.append((os.path.basename(evil_file), str(e)))

    error_messages = []
    if clean_failed:
        failed_names = [f[0] for f in clean_failed]
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_names)}")

    if evil_failed:
        failed_names = [f[0] for f in evil_failed]
        error_messages.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted. Offending files: {', '.join(failed_names)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))
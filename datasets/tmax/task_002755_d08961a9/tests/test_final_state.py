# test_final_state.py
import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/audit.sh"
CLEAN_CORPUS_DIR = "/app/corpus/clean/"
EVIL_CORPUS_DIR = "/app/corpus/evil/"

def test_script_exists_and_executable():
    """Ensure the audit script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def run_script(file_path):
    """Helper to run the script and get its stripped stdout."""
    result = subprocess.run(
        [SCRIPT_PATH, file_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()

def test_adversarial_corpus():
    """
    Test the script against the clean and evil corpora.
    Clean files must output 'CLEAN'.
    Evil files must output 'EVIL'.
    """
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))

    assert len(clean_files) > 0, f"No clean files found in {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No evil files found in {EVIL_CORPUS_DIR}"

    clean_failures = []
    for clean_file in clean_files:
        output = run_script(clean_file)
        if output != "CLEAN":
            basename = os.path.basename(clean_file)
            clean_failures.append(f"{basename} (got {output!r})")

    evil_failures = []
    for evil_file in evil_files:
        output = run_script(evil_file)
        if output != "EVIL":
            basename = os.path.basename(evil_file)
            evil_failures.append(f"{basename} (got {output!r})")

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))
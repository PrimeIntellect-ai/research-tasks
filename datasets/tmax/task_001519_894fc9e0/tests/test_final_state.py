# test_final_state.py

import os
import subprocess
import pytest

EVIL_CORPUS_DIR = "/app/corpora/evil"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
SCRIPT_PATH = "/home/user/detector.py"

def run_detector(csv_path):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, csv_path],
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip()

def test_detector_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_adversarial_corpus():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]

    bypassed_evil = []
    modified_clean = []

    for evil_file in evil_files:
        stdout, _ = run_detector(evil_file)
        if stdout != "SUSPICIOUS":
            bypassed_evil.append((os.path.basename(evil_file), stdout))

    for clean_file in clean_files:
        stdout, _ = run_detector(clean_file)
        if stdout != "OK":
            modified_clean.append((os.path.basename(clean_file), stdout))

    error_messages = []
    if bypassed_evil:
        files_str = ", ".join(f"{f} (output: {out})" for f, out in bypassed_evil)
        error_messages.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {files_str}")

    if modified_clean:
        files_str = ", ".join(f"{f} (output: {out})" for f, out in modified_clean)
        error_messages.append(f"{len(modified_clean)} of {len(clean_files)} clean modified (rejected): {files_str}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))
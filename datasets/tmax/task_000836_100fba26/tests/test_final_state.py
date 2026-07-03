# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/analyze_primer.sh"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"The script {SCRIPT_PATH} is not executable."

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.fasta"))
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.fasta"))

    assert len(clean_files) > 0, "No clean FASTA files found in corpus."
    assert len(evil_files) > 0, "No evil FASTA files found in corpus."

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([SCRIPT_PATH, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([SCRIPT_PATH, f], capture_output=True)
        if result.returncode == 0:
            evil_failures.append(os.path.basename(f))

    errors = []
    if evil_failures:
        errors.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        errors.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}")

    if errors:
        pytest.fail(" | ".join(errors))
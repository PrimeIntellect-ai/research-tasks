# test_final_state.py

import os
import glob
import subprocess
import pytest

SCRIPT_PATH = "/home/user/filter_fasta.sh"
EVIL_CORPUS_DIR = "/app/evil"
CLEAN_CORPUS_DIR = "/app/clean"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def test_adversarial_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.fasta"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.fasta"))

    assert len(evil_files) > 0, f"No files found in evil corpus {EVIL_CORPUS_DIR}"
    assert len(clean_files) > 0, f"No files found in clean corpus {CLEAN_CORPUS_DIR}"

    evil_bypassed = []
    clean_rejected = []

    for evil_file in evil_files:
        result = subprocess.run([SCRIPT_PATH, evil_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "REJECT":
            evil_bypassed.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        result = subprocess.run([SCRIPT_PATH, clean_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "ACCEPT":
            clean_rejected.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        errors.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_rejected)}")

    assert not errors, " | ".join(errors)
# test_final_state.py

import os
import subprocess
import glob
import pytest

GO_SCRIPT = "/home/user/check_matrix.go"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_go_script_exists():
    assert os.path.isfile(GO_SCRIPT), f"The Go script was not found at {GO_SCRIPT}."

def test_adversarial_corpus():
    assert os.path.isfile(GO_SCRIPT), "Cannot test corpus without the Go script."

    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.csv"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.csv"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for f in clean_files:
        result = subprocess.run(["go", "run", GO_SCRIPT, f], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        result = subprocess.run(["go", "run", GO_SCRIPT, f], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(os.path.basename(f))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified (rejected instead of accepted): {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed (accepted instead of rejected): {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))
# test_final_state.py

import os
import subprocess
import pytest

VALIDATOR_SCRIPT = "/home/user/query_validator.py"
EVIL_CORPUS_DIR = "/app/eval_corpus/evil"
CLEAN_CORPUS_DIR = "/app/eval_corpus/clean"

def run_validator(filepath):
    """Runs the student's validator script on a given file and returns the stripped output."""
    result = subprocess.run(
        ["python3", VALIDATOR_SCRIPT, filepath],
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip()

def test_validator_script_exists():
    assert os.path.isfile(VALIDATOR_SCRIPT), f"Validator script missing at {VALIDATOR_SCRIPT}"

def test_adversarial_corpus():
    assert os.path.isfile(VALIDATOR_SCRIPT), "Validator script missing."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.sql')]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.sql')]

    bypassed_evil = []
    rejected_clean = []

    for evil_file in evil_files:
        stdout, _ = run_validator(evil_file)
        if stdout != "REJECT":
            bypassed_evil.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        stdout, _ = run_validator(clean_file)
        if stdout != "ACCEPT":
            rejected_clean.append(os.path.basename(clean_file))

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if rejected_clean:
        errors.append(f"{len(rejected_clean)} of {len(clean_files)} clean rejected: {', '.join(rejected_clean)}")

    assert not errors, " | ".join(errors)
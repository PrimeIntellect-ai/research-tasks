# test_final_state.py

import os
import subprocess
import glob
import pytest

EXECUTABLE = "/home/user/query_sanitizer"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_executable_exists_and_is_executable():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def run_sanitizer(filepath):
    result = subprocess.run(
        [EXECUTABLE, filepath],
        capture_output=True,
        text=True,
        timeout=5
    )
    return result.stdout.strip()

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))

    assert len(clean_files) > 0, f"No JSON files found in clean corpus {CLEAN_CORPUS_DIR}"
    assert len(evil_files) > 0, f"No JSON files found in evil corpus {EVIL_CORPUS_DIR}"

    clean_failed = []
    for filepath in clean_files:
        output = run_sanitizer(filepath)
        if output != "ACCEPT":
            clean_failed.append((os.path.basename(filepath), output))

    evil_failed = []
    for filepath in evil_files:
        output = run_sanitizer(filepath)
        if output != "REJECT":
            evil_failed.append((os.path.basename(filepath), output))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: " + ", ".join(f"{f} (got {out})" for f, out in clean_failed))
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: " + ", ".join(f"{f} (got {out})" for f, out in evil_failed))

    assert not errors, "\n".join(errors)
# test_final_state.py

import os
import subprocess
import pytest

EXECUTABLE_PATH = "/home/user/rust_linter/target/release/rust_linter"
EVAL_CLEAN_DIR = "/home/user/corpora/eval_clean"
EVAL_EVIL_DIR = "/home/user/corpora/eval_evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE_PATH), f"Executable not found at {EXECUTABLE_PATH}. Did you run 'cargo build --release'?"
    assert os.access(EXECUTABLE_PATH, os.X_OK), f"File at {EXECUTABLE_PATH} is not executable."

def test_adversarial_corpus():
    assert os.path.isdir(EVAL_CLEAN_DIR), f"Clean eval corpus missing: {EVAL_CLEAN_DIR}"
    assert os.path.isdir(EVAL_EVIL_DIR), f"Evil eval corpus missing: {EVAL_EVIL_DIR}"

    clean_files = [os.path.join(EVAL_CLEAN_DIR, f) for f in os.listdir(EVAL_CLEAN_DIR) if os.path.isfile(os.path.join(EVAL_CLEAN_DIR, f))]
    evil_files = [os.path.join(EVAL_EVIL_DIR, f) for f in os.listdir(EVAL_EVIL_DIR) if os.path.isfile(os.path.join(EVAL_EVIL_DIR, f))]

    assert len(clean_files) > 0, "No files found in clean eval corpus."
    assert len(evil_files) > 0, "No files found in evil eval corpus."

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run([EXECUTABLE_PATH, cf], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run([EXECUTABLE_PATH, ef], capture_output=True)
        if res.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean files modified/rejected (expected exit code 0): {', '.join(failed_clean)}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed/accepted (expected exit code 1): {', '.join(failed_evil)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))
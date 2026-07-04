# test_final_state.py

import os
import subprocess
import pytest

CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
PROVISIONER_BIN = "/home/user/provisioner/target/release/provisioner"

def test_provisioner_binary_exists():
    """Ensure the provisioner binary has been compiled in release mode."""
    assert os.path.isfile(PROVISIONER_BIN), f"Provisioner binary not found at {PROVISIONER_BIN}. Did you build in release mode?"
    assert os.access(PROVISIONER_BIN, os.X_OK), f"Provisioner binary at {PROVISIONER_BIN} is not executable."

def test_clean_corpus():
    """Ensure the provisioner accepts all valid profiles in the clean corpus."""
    if not os.path.isfile(PROVISIONER_BIN):
        pytest.fail(f"Missing binary {PROVISIONER_BIN}")

    failed_clean = []
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]

    for f in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, f)
        result = subprocess.run([PROVISIONER_BIN, filepath], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(f)

    if failed_clean:
        pytest.fail(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(failed_clean)}")

def test_evil_corpus():
    """Ensure the provisioner firmly rejects all malformed profiles in the evil corpus."""
    if not os.path.isfile(PROVISIONER_BIN):
        pytest.fail(f"Missing binary {PROVISIONER_BIN}")

    bypassed_evil = []
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]

    for f in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, f)
        result = subprocess.run([PROVISIONER_BIN, filepath], capture_output=True)
        if result.returncode == 0:
            bypassed_evil.append(f)

    if bypassed_evil:
        pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed_evil)}")
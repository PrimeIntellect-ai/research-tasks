# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/audit.sh"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_audit_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_clean_corpus_allow():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".json")]
    assert len(clean_files) > 0, f"No JSON files found in {CLEAN_CORPUS_DIR}"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True, text=True)

        output = result.stdout.strip()
        if result.returncode != 0 or output != "ALLOW":
            failed_files.append((filename, result.returncode, output))

    if failed_files:
        details = ", ".join([f"{f} (code {c}, out {o})" for f, c, o in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files failed (expected ALLOW). Details: {details}")

def test_evil_corpus_deny():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".json")]
    assert len(evil_files) > 0, f"No JSON files found in {EVIL_CORPUS_DIR}"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        result = subprocess.run([SCRIPT_PATH, filepath], capture_output=True, text=True)

        output = result.stdout.strip()
        if result.returncode != 0 or output != "DENY":
            failed_files.append((filename, result.returncode, output))

    if failed_files:
        details = ", ".join([f"{f} (code {c}, out {o})" for f, c, o in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected DENY). Details: {details}")
# test_final_state.py
import os
import subprocess
import pytest

CLEAN_DIR = "/home/user/app/corpus/clean"
EVIL_DIR = "/home/user/app/corpus/evil"
LINTER_PATH = "/home/user/app/abi_linter.sh"

def test_linter_exists_and_executable():
    assert os.path.isfile(LINTER_PATH), f"Linter script {LINTER_PATH} does not exist."
    assert os.access(LINTER_PATH, os.X_OK), f"Linter script {LINTER_PATH} is not executable."

def test_adversarial_corpus_clean():
    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert clean_files, f"No files found in clean corpus directory {CLEAN_DIR}."

    modified_clean = []
    for f in clean_files:
        result = subprocess.run([LINTER_PATH, f], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != "ACCEPT":
            modified_clean.append((os.path.basename(f), result.returncode, result.stdout.strip()))

    if modified_clean:
        details = ", ".join([f"{name} (code {code}, out: {out})" for name, code, out in modified_clean])
        pytest.fail(f"{len(modified_clean)} of {len(clean_files)} clean files rejected: {details}")

def test_adversarial_corpus_evil():
    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert evil_files, f"No files found in evil corpus directory {EVIL_DIR}."

    bypassed_evil = []
    for f in evil_files:
        result = subprocess.run([LINTER_PATH, f], capture_output=True, text=True)
        if result.returncode != 1 or result.stdout.strip() != "REJECT":
            bypassed_evil.append((os.path.basename(f), result.returncode, result.stdout.strip()))

    if bypassed_evil:
        details = ", ".join([f"{name} (code {code}, out: {out})" for name, code, out in bypassed_evil])
        pytest.fail(f"{len(bypassed_evil)} of {len(evil_files)} evil files bypassed: {details}")
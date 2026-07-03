# test_final_state.py

import os
import subprocess
import pytest

EVIL_DIR = "/app/corpus/evil/"
CLEAN_DIR = "/app/corpus/clean/"
SANITISER_BIN = "/home/user/sanitiser"
SANITISER_SRC = "/home/user/sanitiser.cpp"

@pytest.fixture(scope="session", autouse=True)
def ensure_sanitiser():
    if not os.path.exists(SANITISER_BIN):
        assert os.path.exists(SANITISER_SRC), f"Sanitiser source not found at {SANITISER_SRC} and binary not found at {SANITISER_BIN}"
        compile_proc = subprocess.run(
            ["g++", "-O2", SANITISER_SRC, "-o", SANITISER_BIN],
            capture_output=True,
            text=True
        )
        assert compile_proc.returncode == 0, f"Failed to compile {SANITISER_SRC}:\n{compile_proc.stderr}"
    assert os.access(SANITISER_BIN, os.X_OK), f"Sanitiser binary at {SANITISER_BIN} is not executable"

def test_clean_corpus_accepted():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))]
    assert clean_files, f"Clean corpus directory is empty: {CLEAN_DIR}"

    failed_files = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_DIR, filename)
        proc = subprocess.run([SANITISER_BIN, filepath], capture_output=True)
        if proc.returncode != 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (exit code != 0): {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    evil_files = [f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))]
    assert evil_files, f"Evil corpus directory is empty: {EVIL_DIR}"

    failed_files = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_DIR, filename)
        proc = subprocess.run([SANITISER_BIN, filepath], capture_output=True)
        if proc.returncode == 0:
            failed_files.append(filename)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed the sanitiser (exit code == 0): {', '.join(failed_files)}")
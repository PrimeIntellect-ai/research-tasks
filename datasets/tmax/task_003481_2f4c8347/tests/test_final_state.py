# test_final_state.py

import os
import subprocess
import pytest

CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"
EXECUTABLE = "/app/auditor-tool/build/validator"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}. Did the build succeed?"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable."

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]
    assert len(clean_files) > 0, "No clean tokens found in corpus."

    failed_files = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, f)
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "VALID":
            failed_files.append(f)

    if failed_files:
        msg = f"{len(failed_files)} of {len(clean_files)} clean tokens rejected or modified.\n"
        msg += "Offending files: " + ", ".join(failed_files)
        pytest.fail(msg)

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    assert len(evil_files) > 0, "No evil tokens found in corpus."

    failed_files = []
    for f in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, f)
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "INVALID":
            failed_files.append(f)

    if failed_files:
        msg = f"{len(failed_files)} of {len(evil_files)} evil tokens bypassed.\n"
        msg += "Offending files: " + ", ".join(failed_files)
        pytest.fail(msg)
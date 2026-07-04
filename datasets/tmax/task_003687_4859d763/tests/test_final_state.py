# test_final_state.py
import os
import subprocess
import pytest

EXECUTABLE = "/home/user/sanitize_query"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}. Did you compile your C program?"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable."

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing: {CLEAN_CORPUS}"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.json')]
    assert len(clean_files) > 0, f"No JSON files found in {CLEAN_CORPUS}"

    failed_files = []
    for f in clean_files:
        file_path = os.path.join(CLEAN_CORPUS, f)
        result = subprocess.run([EXECUTABLE, file_path], capture_output=True)
        if result.returncode != 0:
            failed_files.append(f)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified (rejected). Offending files: {', '.join(failed_files)}")

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing: {EVIL_CORPUS}"
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.json')]
    assert len(evil_files) > 0, f"No JSON files found in {EVIL_CORPUS}"

    bypassed_files = []
    for f in evil_files:
        file_path = os.path.join(EVIL_CORPUS, f)
        result = subprocess.run([EXECUTABLE, file_path], capture_output=True)
        if result.returncode == 0:
            bypassed_files.append(f)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed (accepted). Offending files: {', '.join(bypassed_files)}")
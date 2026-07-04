# test_final_state.py
import os
import subprocess
import pytest

EXECUTABLE = "/home/user/detector/target/release/detector"
EVIL_CORPUS = "/app/evaluation_corpus/evil"
CLEAN_CORPUS = "/app/evaluation_corpus/clean"

def test_executable_exists():
    assert os.path.exists(EXECUTABLE), f"Executable not found at {EXECUTABLE}. Did you compile in release mode?"
    assert os.path.isfile(EXECUTABLE), f"Expected {EXECUTABLE} to be a file."
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable."

def test_evil_corpus():
    assert os.path.isdir(EVIL_CORPUS), f"Evil corpus directory missing at {EVIL_CORPUS}"
    evil_files = sorted([f for f in os.listdir(EVIL_CORPUS) if f.endswith('.json')])
    assert len(evil_files) > 0, "No evil files found in corpus."

    bypassed = []
    for f in evil_files:
        filepath = os.path.join(EVIL_CORPUS, f)
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)

        # Criteria: exit code 1 and stdout contains EVIL
        if result.returncode != 1 or "EVIL" not in result.stdout:
            bypassed.append(f)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending file basenames: {', '.join(bypassed)}")

def test_clean_corpus():
    assert os.path.isdir(CLEAN_CORPUS), f"Clean corpus directory missing at {CLEAN_CORPUS}"
    clean_files = sorted([f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.json')])
    assert len(clean_files) > 0, "No clean files found in corpus."

    modified = []
    for f in clean_files:
        filepath = os.path.join(CLEAN_CORPUS, f)
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)

        # Criteria: exit code 0 and stdout contains CLEAN
        if result.returncode != 0 or "CLEAN" not in result.stdout:
            modified.append(f)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified. Offending file basenames: {', '.join(modified)}")
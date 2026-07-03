# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/traffic_filter"
EVIL_CORPUS = "/app/corpus/evil"
CLEAN_CORPUS = "/app/corpus/clean"

def test_binary_exists():
    assert os.path.exists(BINARY_PATH), f"Compiled binary not found at {BINARY_PATH}. Did you compile your C code?"
    assert os.path.isfile(BINARY_PATH), f"{BINARY_PATH} is not a file."
    assert os.access(BINARY_PATH, os.X_OK), f"{BINARY_PATH} is not executable."

def test_evil_corpus_rejected():
    assert os.path.exists(EVIL_CORPUS), f"Evil corpus directory missing: {EVIL_CORPUS}"
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if os.path.isfile(os.path.join(EVIL_CORPUS, f))]
    assert len(evil_files) > 0, "No files found in evil corpus."

    failures = []
    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS, filename)
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True)
        output = result.stdout.strip()

        if result.returncode != 1 or output != "EVIL":
            failures.append(f"{filename} (exit code: {result.returncode}, output: {output!r})")

    if failures:
        pytest.fail(f"{len(failures)} of {len(evil_files)} evil files bypassed the filter:\n" + "\n".join(failures))

def test_clean_corpus_accepted():
    assert os.path.exists(CLEAN_CORPUS), f"Clean corpus directory missing: {CLEAN_CORPUS}"
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if os.path.isfile(os.path.join(CLEAN_CORPUS, f))]
    assert len(clean_files) > 0, "No files found in clean corpus."

    failures = []
    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS, filename)
        result = subprocess.run([BINARY_PATH, filepath], capture_output=True, text=True)
        output = result.stdout.strip()

        if result.returncode != 0 or output != "CLEAN":
            failures.append(f"{filename} (exit code: {result.returncode}, output: {output!r})")

    if failures:
        pytest.fail(f"{len(failures)} of {len(clean_files)} clean files were incorrectly flagged or failed:\n" + "\n".join(failures))
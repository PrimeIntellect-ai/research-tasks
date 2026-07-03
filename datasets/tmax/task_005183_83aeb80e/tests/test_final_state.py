# test_final_state.py
import os
import subprocess
import pytest

EXECUTABLE = "/home/user/artifact_filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable {EXECUTABLE} does not exist. Did you compile your C program?"
    assert os.access(EXECUTABLE, os.X_OK), f"File {EXECUTABLE} is not executable."

def test_clean_corpus_accepted():
    if not os.path.isfile(EXECUTABLE):
        pytest.skip("Executable missing")

    clean_bundles = [os.path.join(CLEAN_CORPUS_DIR, d) for d in os.listdir(CLEAN_CORPUS_DIR) 
                     if os.path.isdir(os.path.join(CLEAN_CORPUS_DIR, d))]

    assert len(clean_bundles) > 0, "No clean bundles found in the corpus."

    failed_clean = []
    for bundle in clean_bundles:
        result = subprocess.run([EXECUTABLE, bundle], capture_output=True)
        if result.returncode != 0:
            failed_clean.append((os.path.basename(bundle), result.returncode))

    if failed_clean:
        details = ", ".join([f"{name} (exit code {code})" for name, code in failed_clean])
        pytest.fail(f"{len(failed_clean)} of {len(clean_bundles)} clean bundles were incorrectly rejected: {details}")

def test_evil_corpus_rejected():
    if not os.path.isfile(EXECUTABLE):
        pytest.skip("Executable missing")

    evil_bundles = [os.path.join(EVIL_CORPUS_DIR, d) for d in os.listdir(EVIL_CORPUS_DIR) 
                    if os.path.isdir(os.path.join(EVIL_CORPUS_DIR, d))]

    assert len(evil_bundles) > 0, "No evil bundles found in the corpus."

    failed_evil = []
    for bundle in evil_bundles:
        result = subprocess.run([EXECUTABLE, bundle], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(bundle))

    if failed_evil:
        details = ", ".join(failed_evil)
        pytest.fail(f"{len(failed_evil)} of {len(evil_bundles)} evil bundles bypassed the filter (returned 0): {details}")
# test_final_state.py
import os
import subprocess
import glob
import pytest

FILTER_BIN = "/home/user/filter"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
EVIL_CORPUS_DIR = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(FILTER_BIN), f"Executable not found at {FILTER_BIN}"
    assert os.access(FILTER_BIN, os.X_OK), f"File at {FILTER_BIN} is not executable"

def test_openmp_linked():
    # Check if the binary is linked against libomp or libgomp
    result = subprocess.run(["ldd", FILTER_BIN], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run ldd on {FILTER_BIN}"
    assert "omp" in result.stdout.lower(), "Executable does not appear to be linked with OpenMP (-fopenmp)"

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*"))
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*"))

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    clean_failures = []
    for f in clean_files:
        result = subprocess.run([FILTER_BIN, f], capture_output=True)
        if result.returncode != 0:
            clean_failures.append(os.path.basename(f))

    evil_failures = []
    for f in evil_files:
        result = subprocess.run([FILTER_BIN, f], capture_output=True)
        if result.returncode != 1:
            evil_failures.append(os.path.basename(f))

    error_msg = []
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    assert not error_msg, " | ".join(error_msg)
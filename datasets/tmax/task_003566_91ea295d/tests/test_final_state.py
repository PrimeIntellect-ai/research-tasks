# test_final_state.py
import os
import subprocess
import pytest
import json

EXECUTABLE = "/home/user/router_utility/build/request_validator"
CLEAN_CORPUS = "/app/corpus/clean"
EVIL_CORPUS = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def run_executable(target_dir):
    result = subprocess.run(
        [EXECUTABLE, target_dir],
        capture_output=True,
        text=True,
        timeout=10
    )
    assert result.returncode == 0, f"Executable failed with return code {result.returncode}\nStderr: {result.stderr}"
    return result.stdout

def test_clean_corpus():
    stdout = run_executable(CLEAN_CORPUS)
    lines = stdout.strip().split('\n')

    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.json')]

    # We expect ACCEPT for all clean files.
    rejected = []
    for line in lines:
        if not line.strip():
            continue
        if "REJECT" in line.upper():
            rejected.append(line)

    if rejected:
        pytest.fail(f"{len(rejected)} of {len(clean_files)} clean requests were incorrectly REJECTED.\nSample: {rejected[:5]}")

    # Also verify that ACCEPT is present
    accepts = [line for line in lines if "ACCEPT" in line.upper()]
    assert len(accepts) > 0, "No ACCEPT found in clean corpus output."

def test_evil_corpus():
    stdout = run_executable(EVIL_CORPUS)
    lines = stdout.strip().split('\n')

    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.json')]

    # We expect REJECT for all evil files.
    accepted = []
    for line in lines:
        if not line.strip():
            continue
        if "ACCEPT" in line.upper():
            accepted.append(line)

    if accepted:
        pytest.fail(f"{len(accepted)} of {len(evil_files)} evil requests bypassed validation and were ACCEPTED.\nSample: {accepted[:5]}")

    # Also verify that REJECT is present
    rejects = [line for line in lines if "REJECT" in line.upper()]
    assert len(rejects) > 0, "No REJECT found in evil corpus output."
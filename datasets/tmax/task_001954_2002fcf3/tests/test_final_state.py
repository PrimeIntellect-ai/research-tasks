# test_final_state.py

import os
import subprocess
import pytest

DETECTOR_BIN = "/home/user/forensics/detector/target/release/detector"
HIDDEN_EVIL_DIR = "/app/verifier/hidden_evil"
HIDDEN_CLEAN_DIR = "/app/verifier/hidden_clean"

def run_detector(directory):
    assert os.path.isfile(DETECTOR_BIN), f"Detector binary not found at {DETECTOR_BIN}"
    assert os.access(DETECTOR_BIN, os.X_OK), f"Detector binary at {DETECTOR_BIN} is not executable"

    try:
        result = subprocess.run([DETECTOR_BIN, directory], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail(f"Detector binary timed out when analyzing {directory}")

    assert result.returncode == 0, f"Detector binary exited with non-zero code {result.returncode} for {directory}\nStderr: {result.stderr}"

    return result.stdout.splitlines()

def parse_output(lines):
    results = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("EVIL: "):
            filename = line[6:].strip()
            results[filename] = "EVIL"
        elif line.startswith("CLEAN: "):
            filename = line[7:].strip()
            results[filename] = "CLEAN"
    return results

def test_detector_on_hidden_evil():
    assert os.path.isdir(HIDDEN_EVIL_DIR), f"Missing hidden evil corpus directory at {HIDDEN_EVIL_DIR}"
    expected_files = set(os.listdir(HIDDEN_EVIL_DIR))

    lines = run_detector(HIDDEN_EVIL_DIR)
    results = parse_output(lines)

    missed = []
    incorrect = []

    for filename in expected_files:
        if filename not in results:
            missed.append(filename)
        elif results[filename] != "EVIL":
            incorrect.append(filename)

    total = len(expected_files)
    bypassed = len(missed) + len(incorrect)

    error_msg = f"{bypassed} of {total} evil bypassed."
    if missed:
        error_msg += f" Missing output for: {', '.join(missed)}."
    if incorrect:
        error_msg += f" Incorrectly classified as CLEAN: {', '.join(incorrect)}."

    assert bypassed == 0, error_msg

def test_detector_on_hidden_clean():
    assert os.path.isdir(HIDDEN_CLEAN_DIR), f"Missing hidden clean corpus directory at {HIDDEN_CLEAN_DIR}"
    expected_files = set(os.listdir(HIDDEN_CLEAN_DIR))

    lines = run_detector(HIDDEN_CLEAN_DIR)
    results = parse_output(lines)

    missed = []
    incorrect = []

    for filename in expected_files:
        if filename not in results:
            missed.append(filename)
        elif results[filename] != "CLEAN":
            incorrect.append(filename)

    total = len(expected_files)
    modified = len(missed) + len(incorrect)

    error_msg = f"{modified} of {total} clean modified (flagged as evil or missed)."
    if missed:
        error_msg += f" Missing output for: {', '.join(missed)}."
    if incorrect:
        error_msg += f" Incorrectly classified as EVIL: {', '.join(incorrect)}."

    assert modified == 0, error_msg
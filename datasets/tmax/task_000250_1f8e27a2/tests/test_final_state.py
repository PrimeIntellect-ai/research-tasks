# test_final_state.py

import os
import math
import pytest

SCRIPT_PATH = "/home/user/deterministic_integrate.sh"
SAMPLES_PATH = "/home/user/samples.txt"
LOG_PATH = "/home/user/convergence.log"

def compute_expected_log():
    if not os.path.exists(SAMPLES_PATH):
        return []

    with open(SAMPLES_PATH, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = []
    for n in [1000, 2000, 3000, 4000, 5000]:
        subset = lines[:n]
        chunks = [subset[i:i+1000] for i in range(0, len(subset), 1000)]

        partial_sums = []
        for chunk in chunks:
            chunk_sum = sum(math.exp(-(float(x)**2)/2) for x in chunk)
            partial_sums.append(float(f"{chunk_sum:.15f}"))

        final_sum = sum(partial_sums)
        expected.append(f"{n} {final_sum:.15f}")

    return expected

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_contains_parallel_constructs():
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()
    assert "&" in content, f"Script {SCRIPT_PATH} does not contain '&' for background jobs."
    assert "wait" in content, f"Script {SCRIPT_PATH} does not contain 'wait' command."

def test_convergence_log_matches():
    assert os.path.exists(LOG_PATH), f"Log file {LOG_PATH} does not exist."

    with open(LOG_PATH, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    expected_lines = compute_expected_log()

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {LOG_PATH}, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'."
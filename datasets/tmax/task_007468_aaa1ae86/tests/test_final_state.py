# test_final_state.py

import os
import re
import math
import pytest

WORKSPACE_DIR = "/home/user/workspace"
LOG_FILE = os.path.join(WORKSPACE_DIR, "experiment_log.txt")
INFERENCE_CSV = os.path.join(WORKSPACE_DIR, "inference_normalized.csv")

def test_experiment_log_exists_and_format():
    assert os.path.isfile(LOG_FILE), f"File {LOG_FILE} does not exist."

    with open(LOG_FILE, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) >= 1, f"Log file {LOG_FILE} is empty."
    last_line = lines[-1].strip()

    # Expected format: TRAIN_MEAN: 400.5000, TRAIN_STD: 230.9400, INFERENCE_TIME_US: <time>
    pattern = r"^TRAIN_MEAN:\s*400\.5000,\s*TRAIN_STD:\s*230\.9400,\s*INFERENCE_TIME_US:\s*\d+$"
    match = re.match(pattern, last_line)
    assert match is not None, f"Log line '{last_line}' does not match expected format or values (expected mean 400.5000, std 230.9400)."

def test_inference_normalized_csv_contents():
    assert os.path.isfile(INFERENCE_CSV), f"File {INFERENCE_CSV} does not exist."

    with open(INFERENCE_CSV, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 200, f"Expected 200 lines in {INFERENCE_CSV}, got {len(lines)}."

    mean = 400.5
    std = math.sqrt(((800**2) - 1) / 12)

    for i, line in enumerate(lines):
        try:
            val = float(line)
        except ValueError:
            pytest.fail(f"Line {i} in {INFERENCE_CSV} is not a valid float: '{line}'")

        expected = (801 + i - mean) / std
        assert abs(val - expected) < 1e-3, f"Line {i} mismatch: expected {expected:.4f}, got {val}"
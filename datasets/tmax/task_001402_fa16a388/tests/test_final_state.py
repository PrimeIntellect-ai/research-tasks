# test_final_state.py

import os
import re
import pytest

def test_track_sh_exists_and_executable():
    script_path = "/home/user/track.sh"
    assert os.path.isfile(script_path), f"File not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_experiment_log_exists():
    log_path = "/home/user/experiment.log"
    assert os.path.isfile(log_path), f"File not found: {log_path}"

def test_experiment_log_contents():
    log_path = "/home/user/experiment.log"
    assert os.path.isfile(log_path), f"File not found: {log_path}"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected 5 lines in {log_path}, found {len(lines)}"

    expected_seeds = ["10", "20", "30", "40", "50"]

    for i, line in enumerate(lines):
        seed = expected_seeds[i]
        # Check seed matches
        assert f"Seed: {seed}" in line, f"Expected Seed: {seed} in line {i+1}, got: {line}"

        # Check Train_Mean is exactly 0.0000 or -0.0000
        match = re.search(r"Train_Mean:\s*(-?0\.0000)", line)
        assert match is not None, f"Train_Mean is not 0.0000 in line {i+1}: {line}. The data leakage bug might not be correctly fixed."

        # Check Test_Mean exists and is a float
        match_test = re.search(r"Test_Mean:\s*(-?\d+\.\d{4})", line)
        assert match_test is not None, f"Test_Mean format incorrect in line {i+1}: {line}"
# test_final_state.py

import os
import subprocess
import pytest

def test_crash_input_file():
    path = "/home/user/crash_input.txt"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

    with open(path, 'r') as f:
        lines = f.read().strip().splitlines()

    assert len(lines) == 3, f"Expected exactly 3 lines in {path}, got {len(lines)}"

    sum_sq = 0
    for i, line in enumerate(lines):
        line = line.strip()
        assert line.isdigit(), f"Line {i+1} is not a positive integer: '{line}'"
        val = int(line)
        assert val > 0, f"Line {i+1} must be positive, got {val}"
        sum_sq += val * val

    # The sum of squares must exceed the 64-bit signed integer maximum to cause overflow
    max_int64 = 9223372036854775807
    assert sum_sq > max_int64, f"The sum of squares ({sum_sq}) does not exceed 64-bit signed max ({max_int64}) to cause an overflow."

def test_process_logs_script_fixed():
    path = "/home/user/process_logs.sh"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

    with open(path, 'r') as f:
        content = f.read()

    # Check that awk or bc is used for the logic
    assert "bc" in content or "awk" in content, "Script must use 'bc' or 'awk' to handle large number arithmetic."

    # Run the script on latencies.txt to verify it works correctly
    latencies_path = "/home/user/latencies.txt"
    assert os.path.exists(latencies_path), f"Missing {latencies_path}"

    result = subprocess.run([path, latencies_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    output = result.stdout.strip()
    expected_rms = "2867403006.2066"
    assert output == expected_rms, f"Script output incorrect. Expected {expected_rms}, got {output}"

def test_result_file():
    path = "/home/user/result.txt"
    assert os.path.exists(path), f"Missing file: {path}"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_rms = "2867403006.2066"
    assert content == expected_rms, f"Contents of {path} incorrect. Expected {expected_rms}, got {content}"
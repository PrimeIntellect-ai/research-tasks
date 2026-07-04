# test_final_state.py

import os
import subprocess
import pytest

def test_script_executes_successfully():
    script_path = "/home/user/malware_analysis/process_logs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    try:
        result = subprocess.run(
            [script_path],
            capture_output=True,
            text=True,
            timeout=5  # Should complete very quickly if infinite loop and sleep are fixed
        )
        assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("Script execution timed out. Infinite loop or bad date binary issue is likely not fixed.")

def test_intervals_output():
    intervals_path = "/home/user/malware_analysis/intervals.txt"
    assert os.path.isfile(intervals_path), f"File {intervals_path} is missing."

    with open(intervals_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 intervals, but found {len(lines)}."

    expected_intervals = [1.5, 1.6, 2.7, 4.25]
    for i, (actual, expected) in enumerate(zip(lines, expected_intervals)):
        try:
            actual_float = float(actual)
        except ValueError:
            pytest.fail(f"Line {i+1} in {intervals_path} is not a valid float: '{actual}'")

        assert abs(actual_float - expected) < 0.001, f"Interval {i+1} is incorrect. Expected ~{expected}, got {actual_float}."

def test_total_time_output():
    total_path = "/home/user/malware_analysis/total_time.log"
    assert os.path.isfile(total_path), f"File {total_path} is missing."

    with open(total_path, "r") as f:
        content = f.read().strip()

    try:
        total_float = float(content)
    except ValueError:
        pytest.fail(f"Content of {total_path} is not a valid float: '{content}'")

    expected_total = 10.05
    assert abs(total_float - expected_total) < 0.001, f"Total time is incorrect. Expected ~{expected_total}, got {total_float}."
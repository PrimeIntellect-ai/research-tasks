# test_final_state.py
import os
import pytest

def test_anomaly_time_file():
    anomaly_file = "/home/user/anomaly_time.txt"
    assert os.path.isfile(anomaly_file), f"The file {anomaly_file} does not exist."

    with open(anomaly_file, 'r') as f:
        content = f.read().strip()

    assert content == "[02:00:04]", f"The content of {anomaly_file} is incorrect. Expected '[02:00:04]', got '{content}'."

def test_aggregator_cpp_fixed():
    cpp_path = "/home/user/aggregator.cpp"
    assert os.path.isfile(cpp_path), f"The file {cpp_path} does not exist."

    with open(cpp_path, 'r') as f:
        content = f.read()

    # The bug was: for (size_t i = 1; i < batch.size(); i++)
    # It should be fixed to start at 0.
    assert "i = 1;" not in content or "for (size_t i = 0;" in content or "for(size_t i=0;" in content or "for(int i=0;" in content or "for (int i = 0;" in content or "for (auto" in content or "accumulate" in content, \
        "The off-by-one bug in aggregator.cpp does not appear to be fixed correctly."

def test_aggregator_executable_exists():
    exe_path = "/home/user/aggregator"
    assert os.path.isfile(exe_path), f"The compiled executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_service_b_fixed_log_content():
    log_path = "/home/user/logs/service_b_fixed.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[01:59:59] 10",
        "[02:00:04] 108",
        "[02:00:09] 20"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, but found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} in {log_path} is incorrect. Expected '{expected}', got '{lines[i]}'."
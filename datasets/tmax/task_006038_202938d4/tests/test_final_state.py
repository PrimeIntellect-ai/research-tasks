# test_final_state.py

import os
import subprocess
import pytest

RESOLVED_LIST_PATH = "/home/user/resolved_list.txt"
COUNT_BIN_PATH = "/home/user/count_bin"
BENCHMARK_LOG_PATH = "/home/user/benchmark.log"

def test_resolved_list():
    assert os.path.exists(RESOLVED_LIST_PATH), f"File {RESOLVED_LIST_PATH} is missing."
    assert os.path.isfile(RESOLVED_LIST_PATH), f"{RESOLVED_LIST_PATH} is not a file."

    with open(RESOLVED_LIST_PATH, 'r') as f:
        content = f.read().strip()

    expected_lines = [
        "A: 1.5.0",
        "B: 2.5.0",
        "C: 1.1.0",
        "root: 1.0.0"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert actual_lines == expected_lines, f"Contents of {RESOLVED_LIST_PATH} do not match expected resolved packages."

def test_count_bin_executable_and_exit_code():
    assert os.path.exists(COUNT_BIN_PATH), f"Executable {COUNT_BIN_PATH} is missing."
    assert os.path.isfile(COUNT_BIN_PATH), f"{COUNT_BIN_PATH} is not a file."
    assert os.access(COUNT_BIN_PATH, os.X_OK), f"{COUNT_BIN_PATH} is not executable."

    # Run the binary and check exit code
    result = subprocess.run([COUNT_BIN_PATH], capture_output=True)
    assert result.returncode == 4, f"Expected exit code 4, got {result.returncode}."

def test_benchmark_log():
    assert os.path.exists(BENCHMARK_LOG_PATH), f"File {BENCHMARK_LOG_PATH} is missing."
    assert os.path.isfile(BENCHMARK_LOG_PATH), f"{BENCHMARK_LOG_PATH} is not a file."

    with open(BENCHMARK_LOG_PATH, 'r') as f:
        content = f.read()

    assert "Benchmark:" in content, f"{BENCHMARK_LOG_PATH} does not contain 'Benchmark:'."
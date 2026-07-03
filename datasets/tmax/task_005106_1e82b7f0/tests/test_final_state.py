# test_final_state.py

import os
import subprocess
import pytest

def test_sensor_daemon_binary_exists():
    path = "/home/user/sensor_daemon"
    assert os.path.isfile(path), f"Expected compiled binary {path} does not exist."
    assert os.access(path, os.X_OK), f"Expected binary {path} to be executable."

def test_output_log_content():
    path = "/home/user/output.log"
    assert os.path.isfile(path), f"Expected output log {path} does not exist. Did the program run successfully?"

    with open(path, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "Window: 1700000000.000000 to 1700000000.200000, avg: 10.000000",
        "Window: 1700000001.000000 to 1700000001.100000, avg: 20.000000",
        "Window: 1700000003.000000 to 1700000003.150000, avg: 30.000000"
    ]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in output.log, but got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."

def test_valgrind_clean():
    binary = "/home/user/sensor_daemon"
    csv_file = "/home/user/data.csv"

    assert os.path.isfile(binary), "Binary missing, cannot run valgrind."
    assert os.path.isfile(csv_file), "CSV file missing, cannot run valgrind."

    cmd = [
        "valgrind",
        "--leak-check=full",
        "--error-exitcode=1",
        binary,
        csv_file
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail("Valgrind execution timed out. The infinite loop bug might not be fixed.")

    assert result.returncode == 0, (
        "Valgrind reported memory leaks or errors. "
        f"Return code: {result.returncode}\n"
        f"Stderr:\n{result.stderr}"
    )
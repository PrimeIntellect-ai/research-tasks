# test_final_state.py

import os
import pytest

def test_cpp_source_exists():
    source_path = "/home/user/stratified_dedup.cpp"
    assert os.path.isfile(source_path), f"The C++ source file {source_path} does not exist."

def test_executable_exists():
    exec_path = "/home/user/stratified_dedup"
    assert os.path.isfile(exec_path), f"The compiled executable {exec_path} does not exist."
    assert os.access(exec_path, os.X_OK), f"The file {exec_path} is not executable."

def test_investigation_results():
    results_path = "/home/user/investigation_results.txt"
    assert os.path.isfile(results_path), f"The results file {results_path} does not exist."

    expected_output = (
        "[2023-10-01T10:00:06] 192.168.1.6 404 MissingImage\n"
        "[2023-10-01T10:00:00] 192.168.1.1 404 PageNotFound\n"
        "[2023-10-01T10:00:03] 172.16.0.1 500 DatabaseTimeout\n"
        "[2023-10-01T10:00:01] 10.0.0.2 500 InternalServerError\n"
        "[2023-10-01T10:00:10] 192.168.1.10 503 GatewayTimeout\n"
        "[2023-10-01T10:00:05] 192.168.1.5 503 ServiceUnavailable\n"
    )

    with open(results_path, "r") as f:
        actual_content = f.read()

    # Normalize newlines and strip trailing whitespace for robustness
    actual_lines = [line.strip() for line in actual_content.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_output.strip().splitlines()]

    assert actual_lines == expected_lines, (
        f"The content of {results_path} does not match the expected stratified and sorted results.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )
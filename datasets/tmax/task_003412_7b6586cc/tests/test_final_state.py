# test_final_state.py

import os
import math
import pytest

def get_expected_results(log_path):
    expected = []
    with open(log_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                ip = parts[0]
                status = int(parts[2])
                bytes_val = int(parts[3])

                # Simulate the C calculation
                score = 1.0
                epsilon = 0.001
                iterations = 0

                while True:
                    old_score = score
                    score = (score + (bytes_val / float(status + 1))) / 2.0

                    diff = abs(score - old_score)
                    if diff <= epsilon or iterations >= 100:
                        break
                    iterations += 1

                expected.append(f"IP: {ip}, Score: {score:.3f}")
    return expected

def test_results_txt_exists_and_correct():
    results_path = "/home/user/results.txt"
    log_path = "/home/user/server.log"

    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    assert os.path.isfile(results_path), f"Output file {results_path} was not generated."

    expected_lines = get_expected_results(log_path)

    with open(results_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in {results_path}, but found {len(actual_lines)}. "
        "Make sure the date parsing handles both formats correctly."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Line {i+1} in {results_path} is incorrect.\n"
            f"Expected: '{expected}'\n"
            f"Actual:   '{actual}'\n"
            "Check your convergence logic and date parsing."
        )

def test_executable_exists():
    exe_path = "/home/user/log_analyzer"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing. Did you run make?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."
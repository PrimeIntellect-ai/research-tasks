# test_final_state.py

import os
import pytest
import math

APP_DIR = "/home/user/app"
INPUT_STREAM_FILE = os.path.join(APP_DIR, "input_stream.txt")
MATH_LOGIC_FILE = os.path.join(APP_DIR, "math_logic.py")
WORKER_FILE = os.path.join(APP_DIR, "worker.py")
SUCCESS_FILE = os.path.join(APP_DIR, "success.txt")

def test_success_file_exists_and_correct():
    assert os.path.isfile(SUCCESS_FILE), f"Output file {SUCCESS_FILE} does not exist. Did you run run.py?"

    with open(SUCCESS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # The expected output is the square roots of the positive numbers in input_stream.txt
    # 10.0 -> 3.1623, 25.0 -> 5.0000, 16.0 -> 4.0000, 9.0 -> 3.0000, 36.0 -> 6.0000, 49.0 -> 7.0000, 64.0 -> 8.0000, 81.0 -> 9.0000
    expected = ["3.1623", "5.0000", "4.0000", "3.0000", "6.0000", "7.0000", "8.0000", "9.0000"]

    assert len(lines) == len(expected), f"Expected {len(expected)} lines in {SUCCESS_FILE}, but got {len(lines)}."
    for i, (actual, exp) in enumerate(zip(lines, expected)):
        assert actual == exp, f"Line {i+1} in {SUCCESS_FILE} is {actual}, expected {exp}."

def test_math_logic_fixes():
    assert os.path.isfile(MATH_LOGIC_FILE), f"File {MATH_LOGIC_FILE} is missing."
    with open(MATH_LOGIC_FILE, "r") as f:
        content = f.read()

    assert "RuntimeError" in content, "math_logic.py does not raise RuntimeError on convergence failure."
    assert "100" in content, "math_logic.py does not appear to enforce the 100 iterations limit."

def test_worker_fixes():
    assert os.path.isfile(WORKER_FILE), f"File {WORKER_FILE} is missing."
    with open(WORKER_FILE, "r") as f:
        content = f.read()

    assert "RuntimeError" in content, "worker.py does not appear to catch RuntimeError."
    assert "50" in content, "worker.py does not appear to cap the seen_records list at 50."
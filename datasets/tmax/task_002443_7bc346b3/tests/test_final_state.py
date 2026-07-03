# test_final_state.py

import os
import pytest

def test_math_init_conf():
    path = "/home/user/.config/math_init.conf"
    assert os.path.isfile(path), f"Configuration file {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    try:
        val = float(content)
        assert val == 100.0, f"Expected initial state 100.0 in {path}, got {val}"
    except ValueError:
        pytest.fail(f"Configuration file {path} does not contain a valid float: {content}")

def test_recovered_wal():
    path = "/home/user/recovered.wal"
    assert os.path.isfile(path), f"Recovered WAL file {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "ADD 50.0",
        "MUL 2.0",
        "SUB 25.0",
        "ADD 10.0"
    ]

    assert lines == expected_lines, f"Recovered WAL file {path} does not match expected valid lines. Got: {lines}"

def test_result_txt():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"Result file {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
        assert val == 285.0, f"Expected result 285.0 in {path}, got {val}"
    except ValueError:
        pytest.fail(f"Result file {path} does not contain a valid float: {content}")
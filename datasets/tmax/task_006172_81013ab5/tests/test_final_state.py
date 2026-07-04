# test_final_state.py

import os
import re
import pytest

def test_simulator_c_fixed():
    path = "/home/user/simulator.c"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()

    # Check that the buggy line was replaced with the correct one
    assert "dt = 0.01 / (1.0 + fabs(dydt));" in content, "The step-size adaptation rule was not correctly updated."

    # Check that clamping logic is present
    assert "0.0001" in content, "Clamping logic to 0.0001 seems missing."

def test_simulator_binary_exists_and_executable():
    path = "/home/user/simulator"
    assert os.path.exists(path), f"Compiled binary {path} does not exist."
    assert os.access(path, os.X_OK), f"Compiled binary {path} is not executable."

def test_training_data_tsv_content():
    path = "/home/user/training_data.tsv"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "seq2\tGGGGCCCCTTTTAAAA",
        "seq4\tCGTACGTACGTACGTA",
        "seq5\tAAAACCCC"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, found {len(lines)}."

    for expected in expected_lines:
        assert expected in lines, f"Expected line '{expected}' not found in {path}."

def test_training_data_tsv_format():
    path = "/home/user/training_data.tsv"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    # Check that it doesn't contain '>'
    assert ">" not in content, "The output file should not contain '>' characters."

    # Check that sequences are concatenated properly without newlines
    assert "GGGGCCCC\t" not in content and "GGGGCCCC\n" not in content, "Sequences were not properly concatenated on a single line."
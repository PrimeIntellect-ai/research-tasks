# test_final_state.py

import os
import pytest

def test_top5_txt_exists():
    path = "/home/user/top5.txt"
    assert os.path.isfile(path), f"The output file {path} does not exist."

def test_top5_txt_contents():
    output_path = "/home/user/top5.txt"
    expected_path = "/home/user/expected_top5.txt"

    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(expected_path), f"The expected output file {expected_path} does not exist (setup issue)."

    with open(output_path, 'r') as f:
        output_lines = [line.strip() for line in f if line.strip()]

    with open(expected_path, 'r') as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    assert len(output_lines) == 5, f"Expected exactly 5 lines in {output_path}, found {len(output_lines)}."

    for i, (out_line, exp_line) in enumerate(zip(output_lines, expected_lines)):
        assert out_line == exp_line, f"Mismatch at line {i+1}: expected '{exp_line}', got '{out_line}'."
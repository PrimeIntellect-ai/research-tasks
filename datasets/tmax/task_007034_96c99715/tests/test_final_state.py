# test_final_state.py

import os
import pytest

def test_go_program_exists():
    go_prog_path = "/home/user/detect_leakage.go"
    assert os.path.isfile(go_prog_path), f"Expected Go program at {go_prog_path} is missing."

def test_output_file_exists():
    output_path = "/home/user/leaked_experiments.txt"
    assert os.path.isfile(output_path), f"Expected output file at {output_path} is missing."

def test_output_file_content():
    output_path = "/home/user/leaked_experiments.txt"
    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["EXP-002", "EXP-004"]
    assert lines == expected, f"Output file content does not match expected leaked experiments. Got: {lines}, Expected: {expected}"
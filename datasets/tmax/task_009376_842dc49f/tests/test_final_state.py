# test_final_state.py

import os
import pytest

OUTPUT_FILE = "/home/user/output.txt"
INPUTS_FILE = "/home/user/math_processor/inputs.txt"
SECRET = 987654321
MASK_64 = (1 << 64) - 1

def compute_sequence(n: int, secret: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    a = 0
    b = 1
    for _ in range(2, n + 1):
        next_val = (b * secret + a) & MASK_64
        a = b
        b = next_val
    return b

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"The final output file {OUTPUT_FILE} was not created."

def test_output_file_contents():
    assert os.path.isfile(INPUTS_FILE), f"The inputs file {INPUTS_FILE} is missing."

    with open(INPUTS_FILE, "r") as f:
        inputs = [int(line.strip()) for line in f if line.strip()]

    expected_outputs = {str(n): str(compute_sequence(n, SECRET)) for n in inputs}

    with open(OUTPUT_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(inputs), f"Expected {len(inputs)} lines in {OUTPUT_FILE}, but got {len(lines)}."

    for line in lines:
        assert "Input: " in line and ", Output: " in line, f"Output line format is incorrect: '{line}'"
        parts = line.split(", Output: ")
        in_val = parts[0].replace("Input: ", "").strip()
        out_val = parts[1].strip()

        assert in_val in expected_outputs, f"Found unexpected input value '{in_val}' in {OUTPUT_FILE}."
        assert expected_outputs[in_val] == out_val, (
            f"Mismatch for Input: {in_val}. "
            f"Expected Output: {expected_outputs[in_val]}, but got Output: {out_val}."
        )
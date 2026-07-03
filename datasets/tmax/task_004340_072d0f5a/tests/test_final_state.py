# test_final_state.py

import os
import math
import pytest

def compute_expected_power(dna_str):
    mapping = {'A': 1, 'C': 2, 'G': 3, 'T': 4}
    X = 0.0
    Y = 0.0
    for n, char in enumerate(dna_str):
        if char not in mapping:
            continue
        val = mapping[char]
        angle = 2 * math.pi * n / 3
        X += val * math.cos(angle)
        Y += val * math.sin(angle)
    return X**2 + Y**2

def test_analyze_cpp_exists():
    cpp_path = "/home/user/analyze.cpp"
    assert os.path.isfile(cpp_path), f"The C++ source file {cpp_path} does not exist."

def test_power_txt_output():
    dna_path = "/home/user/dna.txt"
    power_path = "/home/user/power.txt"

    assert os.path.isfile(dna_path), f"The input file {dna_path} is missing."
    assert os.path.isfile(power_path), f"The output file {power_path} is missing. Did you run your C++ program?"

    with open(dna_path, 'r') as f:
        dna_content = f.read().strip()

    expected_power = compute_expected_power(dna_content)
    expected_str = f"{expected_power:.2f}"

    with open(power_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_str, \
        f"Incorrect power value in {power_path}. Expected '{expected_str}', got '{actual_content}'."
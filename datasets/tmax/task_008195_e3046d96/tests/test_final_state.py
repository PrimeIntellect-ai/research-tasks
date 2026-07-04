# test_final_state.py

import os
import math
import pytest

def get_expected_result():
    fasta_path = "/home/user/sequence.fasta"
    assert os.path.isfile(fasta_path), f"File missing: {fasta_path}"

    seq = ""
    with open(fasta_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(">"):
                continue
            seq += line

    signal = []
    for c in seq:
        if c == 'A': signal.append(1.0)
        elif c == 'C': signal.append(2.0)
        elif c == 'G': signal.append(-1.0)
        elif c == 'T': signal.append(-2.0)

    N = len(signal)
    mags = []
    for k in range(N):
        re = 0.0
        im = 0.0
        for n in range(N):
            angle = -2.0 * math.pi * k * n / N
            re += signal[n] * math.cos(angle)
            im += signal[n] * math.sin(angle)
        mags.append(math.sqrt(re**2 + im**2))

    s = 0.0
    c = 0.0
    for y in mags:
        y_adj = y - c
        t = s + y_adj
        c = (t - s) - y_adj
        s = t

    return f"{s:.6f}"

def test_result_txt_content():
    """Verify that result.txt exists and contains the correct Kahan sum output."""
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file missing: {result_path}"

    expected_output = get_expected_result()

    with open(result_path, "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Output in result.txt is incorrect. Expected '{expected_output}', got '{actual_output}'"

def test_cpp_modifications():
    """Verify that the C++ code has been modified to use double precision."""
    cpp_path = "/home/user/spectral_analysis.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file missing: {cpp_path}"

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "vector<double>" in content.replace(" ", ""), "The C++ code must use std::vector<double> for the signal."
    assert "double" in content, "The C++ code must use 'double' precision variables."
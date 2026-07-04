# test_final_state.py

import os
import math
import pytest

def compute_expected_sv(filepath):
    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r') as f:
        seqs = [line.strip() for line in f if line.strip()]

    if not seqs:
        return None

    n = len(seqs)
    m = len(seqs[0])

    M = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            c = seqs[i][j]
            if c == 'A': M[i][j] = 1.0
            elif c == 'C': M[i][j] = -1.0
            elif c == 'G': M[i][j] = 2.0
            elif c == 'T': M[i][j] = -2.0

    A = [[0.0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            for k in range(n):
                A[i][j] += M[k][i] * M[k][j]

    v = [1.0] * m
    for _ in range(1000):
        u = [0.0] * m
        norm = 0.0
        for i in range(m):
            for j in range(m):
                u[i] += A[i][j] * v[j]
            norm += u[i] * u[i]
        norm = math.sqrt(norm)
        for i in range(m):
            v[i] = u[i] / norm

    lam = 0.0
    for i in range(m):
        Av_i = 0.0
        for j in range(m):
            Av_i += A[i][j] * v[j]
        lam += v[i] * Av_i

    return math.sqrt(lam)

def test_result_file_exists_and_correct():
    result_path = "/home/user/result.txt"
    primers_path = "/home/user/primers.txt"

    assert os.path.isfile(result_path), f"Missing file: {result_path}. Did you run the compiled program and save the output?"

    expected_sv = compute_expected_sv(primers_path)
    assert expected_sv is not None, f"Could not compute expected value from {primers_path}"

    expected_str = f"{expected_sv:.3f}"

    with open(result_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_str, f"Incorrect output in {result_path}. Expected {expected_str}, got {actual_content}."

def test_code_was_fixed():
    cpp_path = "/home/user/spectral_align.cpp"
    assert os.path.isfile(cpp_path), f"Missing file: {cpp_path}"

    with open(cpp_path, 'r') as f:
        content = f.read()

    assert "sqrt(" in content, "It seems the bug in spectral_align.cpp was not fixed. The output should be the square root of the eigenvalue."
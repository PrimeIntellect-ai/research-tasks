# test_final_state.py
import os
import pytest

def compute_expected_integral(fasta_path):
    if not os.path.exists(fasta_path):
        return None

    with open(fasta_path, 'r') as f:
        lines = f.readlines()

    seq = ""
    for line in lines:
        line = line.strip()
        if not line.startswith(">"):
            seq += line

    mapping = {'A': 1.0, 'C': 2.0, 'G': 3.0, 'T': 4.0}
    X = [mapping[c] for c in seq if c in mapping]
    N = len(X)
    if N == 0:
        return 0.0

    Y = [0.0] * N
    for i in range(N):
        left = X[i-1] if i - 1 >= 0 else 0.0
        right = X[i+1] if i + 1 < N else 0.0
        Y[i] = left + 2.0 * X[i] + right

    if N == 1:
        return Y[0]

    integral = (Y[0] / 2.0) + sum(Y[1:N-1]) + (Y[N-1] / 2.0)
    return integral

def test_process_c_exists_and_uses_openmp():
    c_file = "/home/user/process.c"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."

    with open(c_file, 'r') as f:
        content = f.read()

    assert "omp.h" in content or "omp " in content, f"The file {c_file} does not appear to use OpenMP."

def test_integral_result_correct():
    result_file = "/home/user/integral_result.txt"
    fasta_file = "/home/user/dna.fasta"

    assert os.path.isfile(result_file), f"Result file {result_file} is missing."

    expected_integral = compute_expected_integral(fasta_file)
    assert expected_integral is not None, f"Input FASTA file {fasta_file} is missing."

    expected_str = f"{expected_integral:.1f}"

    with open(result_file, 'r') as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected integral result '{expected_str}', but got '{actual_str}' in {result_file}."
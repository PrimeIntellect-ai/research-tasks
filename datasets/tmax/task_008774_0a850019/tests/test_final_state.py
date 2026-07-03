# test_final_state.py

import os
import math
import itertools

def test_top_singular_values_exists_and_format():
    """Test that top_singular_values.txt exists and has exactly two float values."""
    file_path = "/home/user/top_singular_values.txt"
    assert os.path.isfile(file_path), f"File missing: {file_path}"

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {file_path}, found {len(lines)}"

    try:
        s1 = float(lines[0])
        s2 = float(lines[1])
    except ValueError:
        assert False, f"Values in {file_path} are not valid floats."

    assert s1 >= s2, "Singular values should be sorted in descending order."

def test_norms_exists_and_format():
    """Test that norms.txt exists and has two comma-separated float values."""
    file_path = "/home/user/norms.txt"
    assert os.path.isfile(file_path), f"File missing: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 2, f"Expected 2 comma-separated values in {file_path}, found {len(parts)}"

    try:
        full_norm = float(parts[0])
        rank2_norm = float(parts[1])
    except ValueError:
        assert False, f"Values in {file_path} are not valid floats."

def test_correctness_of_values():
    """
    Recompute the k-mer matrix and its Frobenius norm to validate the student's results.
    Also verify that the rank-2 norm matches the sum of squares of the top 2 singular values.
    """
    fasta_path = "/home/user/sequences.fasta"
    assert os.path.isfile(fasta_path), f"File missing: {fasta_path}"

    with open(fasta_path, 'r') as f:
        lines = f.readlines()

    seqs = [lines[i].strip() for i in range(1, len(lines), 2)]

    kmers = ["".join(p) for p in itertools.product('ACGT', repeat=3)]
    kmer_idx = {k: i for i, k in enumerate(kmers)}

    # Build matrix
    N = len(seqs)
    M = [[0.0] * 64 for _ in range(N)]
    for i, seq in enumerate(seqs):
        for j in range(len(seq) - 2):
            kmer = seq[j:j+3]
            if kmer in kmer_idx:
                M[i][kmer_idx[kmer]] += 1.0

    # Center matrix
    col_means = [0.0] * 64
    for j in range(64):
        col_sum = sum(M[i][j] for i in range(N))
        col_means[j] = col_sum / N

    frobenius_sq = 0.0
    for i in range(N):
        for j in range(64):
            val = M[i][j] - col_means[j]
            frobenius_sq += val * val

    expected_full_norm = math.sqrt(frobenius_sq)

    # Read student's outputs
    with open("/home/user/norms.txt", 'r') as f:
        parts = f.read().strip().split(',')
        student_full_norm = float(parts[0])
        student_rank2_norm = float(parts[1])

    with open("/home/user/top_singular_values.txt", 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        s1 = float(lines[0])
        s2 = float(lines[1])

    # Check full norm
    assert math.isclose(student_full_norm, expected_full_norm, rel_tol=1e-3), \
        f"Expected full Frobenius norm to be approx {expected_full_norm:.4f}, but got {student_full_norm}"

    # Check rank-2 norm consistency
    expected_rank2_norm = math.sqrt(s1**2 + s2**2)
    assert math.isclose(student_rank2_norm, expected_rank2_norm, rel_tol=1e-3), \
        f"Rank-2 norm ({student_rank2_norm}) does not match sqrt(s1^2 + s2^2) = {expected_rank2_norm:.4f}"
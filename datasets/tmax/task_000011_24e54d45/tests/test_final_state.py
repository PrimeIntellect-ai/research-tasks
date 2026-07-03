# test_final_state.py

import os
import math
import pytest

def compute_expected_stats(fasta_path):
    if not os.path.exists(fasta_path):
        return None

    with open(fasta_path, 'r') as f:
        lines = f.read().strip().split('\n')

    seqs = []
    current_seq = []
    for line in lines:
        if line.startswith('>'):
            if current_seq:
                seqs.append("".join(current_seq))
                current_seq = []
        else:
            current_seq.append(line.strip())
    if current_seq:
        seqs.append("".join(current_seq))

    ratios = []
    for seq in seqs:
        if not seq: continue
        gc = sum(1 for c in seq if c in ('G', 'C', 'g', 'c'))
        ratios.append(gc / len(seq))

    ratios.sort()
    N = len(ratios)

    if N < 2:
        return 0, 0, 0

    dx = 1.0 / (N - 1)
    integral = dx * ( (ratios[0] + ratios[-1]) / 2.0 + sum(ratios[1:-1]) )

    mean = sum(ratios) / N

    variance = sum((r - mean)**2 for r in ratios) / N
    std_dev = math.sqrt(variance)

    z_stat = (mean - 0.5) / (std_dev / math.sqrt(N)) if std_dev > 0 else 0.0

    return integral, mean, z_stat

def test_stats_txt_exists_and_correct():
    fasta_path = "/home/user/sequences.fasta"
    stats_path = "/home/user/stats.txt"

    assert os.path.isfile(stats_path), f"File {stats_path} is missing. The C++ program must generate it."

    integral, mean, z_stat = compute_expected_stats(fasta_path)

    expected_content = (
        f"Integral: {integral:.4f}\n"
        f"Mean: {mean:.4f}\n"
        f"Z-stat: {z_stat:.4f}"
    )

    with open(stats_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Contents of {stats_path} do not match the expected output.\n"
        f"Expected:\n{expected_content}\n\nActual:\n{actual_content}"
    )

def test_cpp_file_exists():
    cpp_path = "/home/user/analyze_gc.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."
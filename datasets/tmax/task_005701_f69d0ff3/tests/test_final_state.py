# test_final_state.py

import os
import math
from collections import Counter

def get_kmers(seq, k=3):
    return [seq[i:i+k] for i in range(len(seq)-k+1)]

def kl_div(X, Y):
    return sum(x * math.log(x / y) for x, y in zip(X, Y))

def compute_expected_jsd(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith(">")]

    assert len(lines) == 2, "Expected exactly two sequence lines in primers.fa"
    seqA, seqB = lines[0], lines[1]

    kmersA = get_kmers(seqA)
    kmersB = get_kmers(seqB)

    countA = Counter(kmersA)
    countB = Counter(kmersB)

    bases = ['A', 'C', 'G', 'T']
    all_kmers = [a+b+c for a in bases for b in bases for c in bases]

    totalA = len(kmersA) + 64
    totalB = len(kmersB) + 64

    P = []
    Q = []

    for kmer in all_kmers:
        P.append((countA.get(kmer, 0) + 1) / totalA)
        Q.append((countB.get(kmer, 0) + 1) / totalB)

    M = [(p + q) / 2.0 for p, q in zip(P, Q)]

    jsd = 0.5 * kl_div(P, M) + 0.5 * kl_div(Q, M)
    return f"{jsd:.6f}"

def test_jsd_result():
    input_file = "/home/user/primers.fa"
    output_file = "/home/user/jsd_result.txt"

    assert os.path.exists(input_file), f"Input file {input_file} does not exist."
    assert os.path.exists(output_file), f"Output file {output_file} does not exist."

    expected_jsd_str = compute_expected_jsd(input_file)

    with open(output_file, "r") as f:
        actual_jsd_str = f.read().strip()

    assert actual_jsd_str == expected_jsd_str, f"Expected JSD value '{expected_jsd_str}', but got '{actual_jsd_str}' in {output_file}."
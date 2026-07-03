# test_final_state.py

import os
import math
import itertools
import pytest

def get_kmer_distribution(seq, k=3):
    kmers = ["".join(p) for p in itertools.product("ACGT", repeat=k)]
    counts = {kmer: 0 for kmer in kmers}
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        if kmer in counts:
            counts[kmer] += 1
    total = sum(counts.values())
    if total == 0:
        return [0.0] * len(kmers)
    return [counts[kmer] / total for kmer in sorted(kmers)]

def kl_divergence(p, q):
    return sum(p[i] * math.log(p[i] / q[i]) for i in range(len(p)) if p[i] > 0)

def jensen_shannon_distance(p, q):
    m = [0.5 * (p[i] + q[i]) for i in range(len(p))]
    jsd = 0.5 * kl_divergence(p, m) + 0.5 * kl_divergence(q, m)
    return math.sqrt(jsd)

def test_analyze_sequences_script_exists():
    path = '/home/user/analyze_sequences.py'
    assert os.path.exists(path), f"Missing script: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"

def test_kmer_plot_exists():
    path = '/home/user/kmer_plot.png'
    assert os.path.exists(path), f"Missing plot file: {path}"
    assert os.path.isfile(path), f"Path is not a file: {path}"
    assert os.path.getsize(path) > 0, f"Plot file {path} is empty"

def test_js_distance_output():
    seq1_path = '/home/user/seq1.txt'
    seq2_path = '/home/user/seq2.txt'
    out_path = '/home/user/js_distance.txt'

    assert os.path.exists(out_path), f"Missing output file: {out_path}"
    assert os.path.isfile(out_path), f"Path is not a file: {out_path}"

    with open(seq1_path, 'r') as f:
        seq1 = f.read().strip()
    with open(seq2_path, 'r') as f:
        seq2 = f.read().strip()

    p = get_kmer_distribution(seq1)
    q = get_kmer_distribution(seq2)
    expected_dist = jensen_shannon_distance(p, q)
    expected_str = f"{expected_dist:.4f}"

    with open(out_path, 'r') as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected JS distance {expected_str}, but got {actual_str}"
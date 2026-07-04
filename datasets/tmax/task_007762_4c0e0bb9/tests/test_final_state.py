# test_final_state.py
import os
import math
import pytest

def test_kl_divergence_output():
    out_path = "/home/user/kl_divergence.txt"
    assert os.path.isfile(out_path), f"Output file missing: {out_path}"

    ref_path = "/home/user/reference.txt"
    opt_path = "/home/user/optimized.txt"

    assert os.path.isfile(ref_path), f"Input file missing: {ref_path}"
    assert os.path.isfile(opt_path), f"Input file missing: {opt_path}"

    with open(ref_path, 'r') as f:
        ref = [float(x) for x in f if x.strip()]

    with open(opt_path, 'r') as f:
        opt = [float(x) for x in f if x.strip()]

    min_val = min(min(ref), min(opt))
    max_val = max(max(ref), max(opt))
    W = (max_val - min_val) / 100.0

    P_counts = [0] * 100
    Q_counts = [0] * 100

    for v in ref:
        idx = int(math.floor((v - min_val) / W))
        if idx >= 100: 
            idx = 99
        P_counts[idx] += 1

    for v in opt:
        idx = int(math.floor((v - min_val) / W))
        if idx >= 100: 
            idx = 99
        Q_counts[idx] += 1

    P = [c / len(ref) for c in P_counts]
    Q = [c / len(opt) for c in Q_counts]

    P_adj = [p + 1e-9 for p in P]
    Q_adj = [q + 1e-9 for q in Q]

    kl = sum(p * math.log(p / q) for p, q in zip(P_adj, Q_adj))
    expected_output = f"{kl:.6f}"

    with open(out_path, 'r') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"Expected KL divergence {expected_output}, but got {actual_output}"
# test_final_state.py

import os
import json
import math
from collections import Counter
import pytest

def read_fasta(filepath):
    seqs = []
    with open(filepath, 'r') as f:
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq:
                    seqs.append("".join(seq))
                    seq = []
            else:
                seq.append(line)
        if seq:
            seqs.append("".join(seq))
    return seqs

def compute_ground_truth(seqs):
    n_seqs = len(seqs)
    out_degrees = [0] * n_seqs
    total_edges = 0

    for i in range(n_seqs):
        for j in range(n_seqs):
            if i == j:
                continue
            s1 = seqs[i]
            s2 = seqs[j]

            # Find longest overlap >= 10
            max_len = min(len(s1), len(s2))
            for length in range(max_len, 9, -1):
                if s1[-length:] == s2[:length]:
                    out_degrees[i] += 1
                    total_edges += 1
                    break

    freqs = Counter(out_degrees)
    x_vals = []
    y_vals = []
    for x, y in freqs.items():
        if y > 0:
            x_vals.append(x)
            y_vals.append(y)

    n = len(x_vals)
    sum_x = sum(x_vals)
    sum_lny = sum(math.log(y) for y in y_vals)
    sum_x_lny = sum(x * math.log(y) for x, y in zip(x_vals, y_vals))
    sum_x2 = sum(x**2 for x in x_vals)

    m = (n * sum_x_lny - sum_x * sum_lny) / (n * sum_x2 - sum_x**2)
    c = (sum_lny - m * sum_x) / n
    A = math.exp(c)
    b = -m

    return n_seqs, total_edges, A, b

def test_final_state():
    fasta_path = "/home/user/sequences.fasta"
    results_path = "/home/user/analysis_results.json"

    assert os.path.exists(fasta_path), f"FASTA file {fasta_path} is missing."
    assert os.path.exists(results_path), f"Results JSON file {results_path} is missing."

    seqs = read_fasta(fasta_path)
    expected_nodes, expected_edges, expected_A, expected_b = compute_ground_truth(seqs)

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {results_path} as JSON.")

    assert "total_nodes" in results, "Missing 'total_nodes' in JSON output."
    assert "total_edges" in results, "Missing 'total_edges' in JSON output."
    assert "A" in results, "Missing 'A' in JSON output."
    assert "b" in results, "Missing 'b' in JSON output."

    assert results["total_nodes"] == expected_nodes, f"Expected total_nodes={expected_nodes}, got {results['total_nodes']}"
    assert results["total_edges"] == expected_edges, f"Expected total_edges={expected_edges}, got {results['total_edges']}"

    assert math.isclose(results["A"], expected_A, rel_tol=1e-3, abs_tol=1e-3), f"Expected A={expected_A}, got {results['A']}"
    assert math.isclose(results["b"], expected_b, rel_tol=1e-3, abs_tol=1e-3), f"Expected b={expected_b}, got {results['b']}"
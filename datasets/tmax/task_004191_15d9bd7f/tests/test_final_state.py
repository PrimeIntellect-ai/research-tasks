# test_final_state.py

import os
import math
import pytest

def test_edges_tsv_correctness():
    edges_file = "/home/user/edges.tsv"
    assert os.path.isfile(edges_file), f"Missing file: {edges_file}"

    with open(edges_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # We expect 6 pairs from 4 sequences (combinations of 2)
    assert len(lines) == 6, f"Expected 6 edges in {edges_file}, found {len(lines)}"

    parsed_edges = {}
    for line in lines:
        parts = line.split('\t')
        assert len(parts) == 3, f"Invalid format in edges.tsv: {line}"
        seq1, seq2, weight = parts
        # normalize pair order
        if seq1 > seq2:
            seq1, seq2 = seq2, seq1
        parsed_edges[(seq1, seq2)] = float(weight)

    # Expected calculations:
    # Seq1 vs Seq2: identical -> dist 0 -> weight 999.00
    assert ('Seq1', 'Seq2') in parsed_edges, "Missing edge Seq1-Seq2"
    assert math.isclose(parsed_edges[('Seq1', 'Seq2')], 999.00, rel_tol=1e-5), \
        f"Expected weight 999.00 for Seq1-Seq2, got {parsed_edges[('Seq1', 'Seq2')]}"

    # Seq1 vs Seq3: dist = 2 -> weight = 0.50
    assert ('Seq1', 'Seq3') in parsed_edges, "Missing edge Seq1-Seq3"
    assert math.isclose(parsed_edges[('Seq1', 'Seq3')], 0.50, rel_tol=1e-2), \
        f"Expected weight ~0.50 for Seq1-Seq3, got {parsed_edges[('Seq1', 'Seq3')]}"

    # Seq1 vs Seq4: dist = 1.333... -> weight = 0.75
    assert ('Seq1', 'Seq4') in parsed_edges, "Missing edge Seq1-Seq4"
    assert math.isclose(parsed_edges[('Seq1', 'Seq4')], 0.75, rel_tol=1e-2), \
        f"Expected weight ~0.75 for Seq1-Seq4, got {parsed_edges[('Seq1', 'Seq4')]}"

def test_histogram_txt_correctness():
    hist_file = "/home/user/histogram.txt"
    assert os.path.isfile(hist_file), f"Missing file: {hist_file}"

    with open(hist_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Based on rounding:
    # 0.50 -> 1
    # 0.75 -> 1
    # 999.00 -> 999
    # We expect exactly two lines in the histogram:
    # 1: *****
    # 999: *

    expected_lines = [
        "1: *****",
        "999: *"
    ]

    assert len(lines) == 2, f"Expected 2 lines in histogram.txt, got {len(lines)}"

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Histogram line {i+1} mismatch. Expected '{expected}', got '{lines[i]}'"
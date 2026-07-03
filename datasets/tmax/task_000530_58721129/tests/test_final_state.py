# test_final_state.py

import math
import json
import os
import pytest

def test_features_json_exists_and_correct():
    """Test that the features.json file exists and contains the correct 4x4 KL divergence matrix."""
    path = "/home/user/features.json"
    assert os.path.exists(path), f"File {path} does not exist. The Rust program must write the output here."

    with open(path, "r") as f:
        try:
            student_matrix = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("features.json is not valid JSON.")

    assert isinstance(student_matrix, list), "features.json must contain a JSON array (list of lists)."
    assert len(student_matrix) == 4, f"features.json must be a 4x4 matrix, but has {len(student_matrix)} rows."

    # Recompute the expected matrix based on the problem description
    seqs = ["ACGTACGTACGT", "CCCGGGGAAAA", "GGGGCC", "AAAAAGGGG"]
    kmers = [c1+c2+c3 for c1 in "ACGT" for c2 in "ACGT" for c3 in "ACGT"]

    vecs = []
    for s in seqs:
        counts = {k: 1e-8 for k in kmers}
        for i in range(len(s)-2):
            kmer = s[i:i+3]
            if kmer in counts:
                counts[kmer] += 1

        total = sum(counts.values())
        vecs.append([counts[k] / total for k in kmers])

    expected_matrix = []
    for i in range(4):
        row = []
        for j in range(4):
            p = vecs[i]
            q = vecs[j]
            kl = sum(p[k] * math.log(p[k] / q[k]) for k in range(64))
            row.append(round(kl, 4))
        expected_matrix.append(row)

    for i in range(4):
        assert isinstance(student_matrix[i], list), f"Row {i} in features.json is not a list."
        assert len(student_matrix[i]) == 4, f"Row {i} in features.json does not have 4 elements."
        for j in range(4):
            student_val = student_matrix[i][j]
            expected_val = expected_matrix[i][j]
            assert isinstance(student_val, (int, float)), f"Element at ({i},{j}) is not a number."
            assert math.isclose(student_val, expected_val, rel_tol=1e-3, abs_tol=1e-3), \
                f"Value at ({i},{j}) is {student_val}, expected {expected_val}."
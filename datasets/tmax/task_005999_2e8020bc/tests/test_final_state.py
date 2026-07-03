# test_final_state.py

import os
import json
import pytest

def solve_linear_system(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    for i in range(n):
        max_el = abs(M[i][i])
        max_row = i
        for k in range(i+1, n):
            if abs(M[k][i]) > max_el:
                max_el = abs(M[k][i])
                max_row = k
        M[i], M[max_row] = M[max_row], M[i]

        for k in range(i+1, n):
            if M[i][i] == 0:
                continue
            c = -M[k][i] / M[i][i]
            for j in range(i, n+1):
                if i == j:
                    M[k][j] = 0
                else:
                    M[k][j] += c * M[i][j]

    x = [0.0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = M[i][n] / M[i][i]
        for k in range(i-1, -1, -1):
            M[k][n] -= M[k][i] * x[i]

    return x

def test_libseq_so_exists():
    lib_path = '/home/user/libseq.so'
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not created."

def test_run_pipeline_exists():
    script_path = '/home/user/run_pipeline.py'
    assert os.path.isfile(script_path), f"Python script {script_path} was not created."

def test_report_json():
    report_path = '/home/user/report.json'
    assert os.path.isfile(report_path), f"Report file {report_path} was not created."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "adjacency_matrix" in report, "Key 'adjacency_matrix' missing from report.json"
    assert "consensus_scores" in report, "Key 'consensus_scores' missing from report.json"

    # Read sequences to compute expected values
    seq_file = '/home/user/data/sequences.txt'
    with open(seq_file, 'r') as f:
        sequences = f.read().splitlines()

    N = len(sequences)
    L = len(sequences[0])

    expected_A = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            dist = sum(1 for a, b in zip(sequences[i], sequences[j]) if a != b)
            expected_A[i][j] = L - dist

    assert report["adjacency_matrix"] == expected_A, "Adjacency matrix in report.json is incorrect."

    # Compute expected consensus scores
    M = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            M[i][j] = 0.05 * expected_A[i][j]
            if i == j:
                M[i][j] += 1.0

    b = [1.0] * N
    expected_x = solve_linear_system(M, b)

    reported_x = report["consensus_scores"]
    assert len(reported_x) == N, "Length of consensus_scores does not match number of sequences."

    for i in range(N):
        expected_val = round(expected_x[i], 4)
        assert abs(reported_x[i] - expected_val) <= 1e-4, f"Consensus score at index {i} is incorrect. Expected {expected_val}, got {reported_x[i]}."
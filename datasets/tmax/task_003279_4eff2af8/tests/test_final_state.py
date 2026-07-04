# test_final_state.py

import os
import math
import pytest

def build_matrix(filename, N):
    adj = [[0.0] * N for _ in range(N)]
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            u, v, w = line.strip().split()
            u, v = int(u), int(v)
            w = float(w)
            adj[u][v] = w
            adj[v][u] = w

    M = [[0.0] * N for _ in range(N)]
    for i in range(N):
        row_sum = sum(adj[i])
        if row_sum > 0:
            for j in range(N):
                M[i][j] = adj[i][j] / row_sum
    return M

def simulate(M, steps=100):
    N = len(M)
    P = [0.0] * N
    P[0] = 1.0
    for _ in range(steps):
        next_P = [0.0] * N
        for i in range(N):
            if P[i] > 0:
                for j in range(N):
                    next_P[j] += P[i] * M[i][j]
        P = next_P

    for i in range(N):
        P[i] += 1e-9

    total = sum(P)
    for i in range(N):
        P[i] /= total

    return P

def compute_expected_kl():
    N = 9
    graph_a_path = "/home/user/graph_A.txt"
    graph_b_path = "/home/user/graph_B.txt"

    M_A = build_matrix(graph_a_path, N)
    M_B = build_matrix(graph_b_path, N)

    P_A = simulate(M_A, 100)
    P_B = simulate(M_B, 100)

    kl = 0.0
    for i in range(N):
        kl += P_A[i] * math.log(P_A[i] / P_B[i])
    return kl

def test_simulate_c_exists():
    """Test that the C source file exists."""
    assert os.path.isfile("/home/user/simulate.c"), "The source file /home/user/simulate.c is missing."

def test_kl_result_exists_and_correct():
    """Test that the kl_result.txt file exists and contains the correct KL divergence value."""
    result_path = "/home/user/kl_result.txt"
    assert os.path.isfile(result_path), f"The output file {result_path} is missing."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content, f"The output file {result_path} is empty."

    try:
        actual_kl = float(content)
    except ValueError:
        pytest.fail(f"The content of {result_path} is not a valid float: '{content}'")

    expected_kl = compute_expected_kl()

    tolerance = 0.000005
    assert abs(actual_kl - expected_kl) <= tolerance, \
        f"The computed KL divergence {actual_kl} differs from the expected {expected_kl:.6f} by more than {tolerance}."
# test_final_state.py
import os
import json
import numpy as np
import scipy.stats

def als_nmf_correct(V, k, max_iter=1000, tol=1e-4, lam=0.1):
    np.random.seed(42)
    n, m = V.shape
    W = np.random.rand(n, k)
    H = np.random.rand(k, m)

    prev_loss = float('inf')

    for _ in range(max_iter):
        H = np.linalg.solve(W.T @ W + lam * np.eye(k), W.T @ V)
        H[H < 0] = 0

        W = np.linalg.solve(H @ H.T + lam * np.eye(k), H @ V.T).T
        W[W < 0] = 0

        loss = np.sum((V - W @ H)**2)
        if abs(prev_loss - loss) < tol:
            break
        prev_loss = loss

    return W, H, loss

def test_convergence_plot_exists():
    assert os.path.isfile('/home/user/convergence.png'), "/home/user/convergence.png is missing or not a file."

def test_results_json():
    json_path = '/home/user/results.json'
    assert os.path.isfile(json_path), f"{json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not a valid JSON file."

    assert "k3_loss" in results, "'k3_loss' missing from results.json"
    assert "k4_loss" in results, "'k4_loss' missing from results.json"
    assert "p_value" in results, "'p_value' missing from results.json"

    # Load data and compute expected values
    csv_path = '/home/user/gene_expression.csv'
    assert os.path.isfile(csv_path), f"{csv_path} is missing."

    V = np.loadtxt(csv_path, delimiter=',')

    W3, H3, loss3 = als_nmf_correct(V, k=3)
    W4, H4, loss4 = als_nmf_correct(V, k=4)

    err3 = np.sum((V - W3 @ H3)**2, axis=1)
    err4 = np.sum((V - W4 @ H4)**2, axis=1)

    _, p_val = scipy.stats.ttest_rel(err3, err4)

    assert abs(results["k3_loss"] - loss3) < 1e-3, f"k3_loss is incorrect. Expected ~{loss3:.5f}, got {results['k3_loss']}"
    assert abs(results["k4_loss"] - loss4) < 1e-3, f"k4_loss is incorrect. Expected ~{loss4:.5f}, got {results['k4_loss']}"
    assert abs(results["p_value"] - p_val) < 1e-3, f"p_value is incorrect. Expected ~{p_val:.5f}, got {results['p_value']}"
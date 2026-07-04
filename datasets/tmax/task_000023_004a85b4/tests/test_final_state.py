# test_final_state.py
import json
import os
import numpy as np
import networkx as nx
from scipy.optimize import curve_fit

def test_final_state():
    # 1. Re-derive the ground truth k_true by running the fixed simulation
    np.random.seed(42)
    G = nx.erdos_renyi_graph(10, 0.3, seed=42)
    L = nx.laplacian_matrix(G).toarray()

    def diffusion(t, y):
        return -0.5 * L.dot(y)

    def adaptive_rk_fixed(func, t_span, y0, tol=1e-6):
        t0, tf = t_span
        t = t0
        y = np.array(y0, dtype=float)
        ts = [t]
        ys = [y.copy()]
        dt = 0.01

        while t < tf:
            if t + dt > tf:
                dt = tf - t

            k1 = dt * func(t, y)
            k2 = dt * func(t + dt/2, y + k1/2)
            k3 = dt * func(t + dt/2, y + k2/2)
            k4 = dt * func(t + dt, y + k3)

            y_next = y + (k1 + 2*k2 + 2*k3 + k4) / 6
            err = np.max(np.abs(k2 - k3)) + 1e-12

            # Fixed formula
            dt_new = dt * min(2.0, max(0.1, (tol / err)**0.2))

            if err <= tol:
                t += dt
                y = y_next
                ts.append(t)
                ys.append(y.copy())

            dt = dt_new

        return np.array(ts), np.array(ys)

    y0 = np.zeros(10)
    y0[0] = 10.0

    t_sim, y_sim = adaptive_rk_fixed(diffusion, (0, 5.0), y0)
    node_0 = y_sim[:, 0]

    def exp_model(t, A, k):
        return A * np.exp(-k * t)

    popt, _ = curve_fit(exp_model, t_sim, node_0, p0=(10.0, 0.5))
    k_true = popt[1]

    # 2. Check the agent's output
    json_path = "/home/user/analysis.json"
    assert os.path.exists(json_path), f"Missing output file: {json_path}"

    with open(json_path, "r") as f:
        data = json.load(f)

    assert "estimated_k" in data, "JSON missing 'estimated_k'"
    assert "better_model" in data, "JSON missing 'better_model'"
    assert "ci_95_lower" in data, "JSON missing 'ci_95_lower'"
    assert "ci_95_upper" in data, "JSON missing 'ci_95_upper'"

    estimated_k = data["estimated_k"]
    better_model = data["better_model"]

    assert better_model == "exponential", f"Expected 'better_model' to be 'exponential', got '{better_model}'"

    error = abs(estimated_k - k_true)
    assert error < 0.05, (
        f"Metric failed: Absolute difference between estimated_k and k_true is {error:.4f}, "
        f"which is >= threshold 0.05. (estimated_k={estimated_k}, k_true={k_true:.4f})"
    )
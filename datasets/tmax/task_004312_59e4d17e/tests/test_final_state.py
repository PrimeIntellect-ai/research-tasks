# test_final_state.py

import os
import json
import pytest

def run_sim(dt):
    dx = 0.1
    alpha = 0.01
    N = 11
    u = [25.0] * N
    P = [0.0] * N
    P[4] = P[5] = P[6] = 1000.0

    steps = int(round(2.0 / dt))

    for _ in range(steps):
        u_new = list(u)
        for i in range(1, N-1):
            d2u = (u[i-1] - 2*u[i] + u[i+1]) / (dx**2)
            u_new[i] = u[i] + dt * (alpha * d2u + P[i])
        u = u_new
    return u

def compute_expected_results():
    dt = 0.1
    prev_center = -1000.0
    optimal_dt = 0.1
    final_u = []

    while True:
        u = run_sim(dt)
        center = u[5]
        if abs(center - prev_center) < 0.01 and dt != 0.1:
            optimal_dt = dt
            final_u = u
            break
        prev_center = center
        dt /= 2.0

    sensor_data_path = "/home/user/sensor_data.txt"
    if not os.path.exists(sensor_data_path):
        # Fallback to default if file is missing for some reason
        sensor = [25.0, 33.1, 48.2, 71.4, 115.6, 142.3, 115.6, 71.4, 48.2, 33.1, 25.0]
    else:
        with open(sensor_data_path, "r") as f:
            sensor = [float(line.strip()) for line in f if line.strip()]

    errors = [final_u[i] - sensor[i] for i in range(11)]
    mean = sum(errors) / 11.0
    variance = sum((e - mean)**2 for e in errors) / 11.0

    return {
        "optimal_dt": optimal_dt,
        "center_temp": final_u[5],
        "error_mean": mean,
        "error_variance": variance
    }

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"Results file not found at {results_path}"

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    expected = compute_expected_results()

    keys = ["optimal_dt", "center_temp", "error_mean", "error_variance"]
    for key in keys:
        assert key in results, f"Missing key '{key}' in {results_path}"

        actual_val = results[key]
        expected_val = expected[key]

        assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a number."
        assert abs(actual_val - expected_val) < 1e-3, \
            f"Mismatch in '{key}': expected approx {expected_val:.4f}, got {actual_val:.4f}"
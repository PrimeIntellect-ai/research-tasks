# test_final_state.py
import os
import json
import math
import pytest

def get_expected_simulated():
    x, y = 3.0, 1.0
    dt = 0.01
    def f(x, y): return -0.5*x + 0.1*y**2
    def g(x, y): return 0.2*x*y - 0.6*y

    for _ in range(5000):
        k1x = f(x, y)
        k1y = g(x, y)

        k2x = f(x + 0.5*dt*k1x, y + 0.5*dt*k1y)
        k2y = g(x + 0.5*dt*k1x, y + 0.5*dt*k1y)

        k3x = f(x + 0.5*dt*k2x, y + 0.5*dt*k2y)
        k3y = g(x + 0.5*dt*k2x, y + 0.5*dt*k2y)

        k4x = f(x + dt*k3x, y + dt*k3y)
        k4y = g(x + dt*k3x, y + dt*k3y)

        x += (dt/6.0) * (k1x + 2*k2x + 2*k3x + k4x)
        y += (dt/6.0) * (k1y + 2*k2y + 2*k3y + k4y)
    return x, y

def test_simulation_results():
    results_path = "/home/user/simulation_results.json"
    assert os.path.exists(results_path), f"Expected results file {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    required_keys = [
        "initial_root_x", "initial_root_y",
        "simulated_final_x", "simulated_final_y",
        "analytical_ss_x", "analytical_ss_y"
    ]

    for key in required_keys:
        assert key in data, f"Missing key '{key}' in JSON output."
        assert isinstance(data[key], (int, float)), f"Value for '{key}' must be a number."

    # 1. Check Initial Root
    assert math.isclose(data["initial_root_x"], 3.0, abs_tol=1e-3), \
        f"initial_root_x is {data['initial_root_x']}, expected ~3.0"
    assert math.isclose(data["initial_root_y"], 1.0, abs_tol=1e-3), \
        f"initial_root_y is {data['initial_root_y']}, expected ~1.0"

    # 2. Check Analytical Steady State
    expected_ss_x = 3.0
    expected_ss_y = math.sqrt(15)
    assert math.isclose(data["analytical_ss_x"], expected_ss_x, abs_tol=1e-3), \
        f"analytical_ss_x is {data['analytical_ss_x']}, expected ~{expected_ss_x}"
    assert math.isclose(data["analytical_ss_y"], expected_ss_y, abs_tol=1e-3), \
        f"analytical_ss_y is {data['analytical_ss_y']}, expected ~{expected_ss_y}"

    # 3. Check Simulated Final State
    expected_sim_x, expected_sim_y = get_expected_simulated()
    assert math.isclose(data["simulated_final_x"], expected_sim_x, abs_tol=1e-3), \
        f"simulated_final_x is {data['simulated_final_x']}, expected ~{expected_sim_x}"
    assert math.isclose(data["simulated_final_y"], expected_sim_y, abs_tol=1e-3), \
        f"simulated_final_y is {data['simulated_final_y']}, expected ~{expected_sim_y}"
# test_final_state.py
import os
import json
import math
import pytest

def euler_sim(dt):
    A = [1.0, 1.0, 1.0]
    k = 0.8
    C_max = 100000.0
    steps = int(round(30.0 / dt))
    for _ in range(steps):
        sum_A = sum(A)
        rate = k * (1.0 - sum_A / C_max)
        A = [a + dt * a * rate for a in A]
    return sum(A)

def test_simulation_results_file_exists():
    path = "/home/user/simulation_results.json"
    assert os.path.exists(path), f"Output file {path} is missing."

def test_simulation_results_content():
    path = "/home/user/simulation_results.json"
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    # Check required keys
    required_keys = {"optimal_dt", "amplicon_lengths", "final_total_concentration", "tv_distance"}
    missing = required_keys - set(data.keys())
    assert not missing, f"JSON is missing keys: {missing}"

    # Verify amplicon lengths
    lengths = sorted(data["amplicon_lengths"])
    assert lengths == [998, 999, 1000], f"Expected amplicon lengths [998, 999, 1000], got {lengths}"

    # Compute baseline and find expected optimal dt
    baseline_total = euler_sim(0.001)
    dts = [1.0, 0.5, 0.1, 0.05, 0.01]
    expected_optimal_dt = None
    for dt in dts:
        total = euler_sim(dt)
        if abs(total - baseline_total) / baseline_total <= 0.005:
            expected_optimal_dt = dt
            break

    assert expected_optimal_dt is not None, "Could not find a valid optimal dt in the test logic."

    # Verify optimal dt
    assert math.isclose(data["optimal_dt"], expected_optimal_dt, rel_tol=1e-5), \
        f"Expected optimal_dt {expected_optimal_dt}, got {data['optimal_dt']}"

    # Verify final total concentration
    expected_total = euler_sim(expected_optimal_dt)
    assert math.isclose(data["final_total_concentration"], expected_total, rel_tol=1e-2), \
        f"Expected final_total_concentration around {expected_total}, got {data['final_total_concentration']}"

    # Verify TV distance
    # P = 1/3 for each
    # Q = 1000: 0.35, 999: 0.35, 998: 0.30
    tv_expected = 0.5 * (abs(1/3 - 0.35) + abs(1/3 - 0.35) + abs(1/3 - 0.30))
    tv_rounded = round(tv_expected, 4)

    assert math.isclose(data["tv_distance"], tv_rounded, abs_tol=0.0005), \
        f"Expected tv_distance around {tv_rounded}, got {data['tv_distance']}"
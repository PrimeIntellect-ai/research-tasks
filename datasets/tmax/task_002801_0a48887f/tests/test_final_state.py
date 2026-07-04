# test_final_state.py

import os
import json
import math
import ctypes
import pytest

def test_results_json_exists():
    assert os.path.exists("/home/user/results.json"), "/home/user/results.json does not exist."

def test_analyze_script_exists():
    assert os.path.exists("/home/user/analyze.py"), "/home/user/analyze.py does not exist."

def test_output_files_exist():
    for n in [16, 32, 64]:
        assert os.path.exists(f"/home/user/output_{n}.txt"), f"/home/user/output_{n}.txt does not exist. Did analyze.py run sim_expression.py?"

def test_results_values():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), "Cannot check values, results.json is missing."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON.")

    assert "sum_64" in results, "Key 'sum_64' missing in results.json"
    assert "kl_div_64" in results, "Key 'kl_div_64' missing in results.json"

    # Compute expected values
    N = 64
    mesh = {}
    for i in range(N):
        for j in range(N):
            mesh[(i, j)] = math.sin(i * math.pi / N) * math.cos(j * math.pi / N) + 1.0

    sorted_keys = sorted(mesh.keys())

    # Compute float32 deterministic sum
    total_sum = ctypes.c_float(0.0)
    for k in sorted_keys:
        val = ctypes.c_float(mesh[k])
        total_sum = ctypes.c_float(total_sum.value + val.value)

    expected_sum_64 = total_sum.value

    # Compute KL divergence
    grid_vals = [mesh[k] for k in sorted_keys]
    sum_grid = sum(grid_vals)
    norm_grid = [v / sum_grid for v in grid_vals]

    uniform_prob = 1.0 / (N * N)
    expected_kl_div = sum(p * math.log(p / uniform_prob) for p in norm_grid if p > 0)

    # Assertions
    assert math.isclose(results["sum_64"], expected_sum_64, rel_tol=1e-4), \
        f"sum_64 is {results['sum_64']}, expected ~{expected_sum_64}. Ensure float32 addition in lexicographical order."

    assert math.isclose(results["kl_div_64"], expected_kl_div, rel_tol=1e-4), \
        f"kl_div_64 is {results['kl_div_64']}, expected ~{expected_kl_div}."
# test_final_state.py
import os
import json
import math
import pytest

def test_required_files_exist():
    required_files = [
        "/home/user/spatial_grid.py",
        "/home/user/run_queries.py",
        "/home/user/benchmark.py",
        "/home/user/test_spatial_grid.py"
    ]
    for file_path in required_files:
        assert os.path.exists(file_path), f"Required file {file_path} is missing."
        assert os.path.isfile(file_path), f"Expected {file_path} to be a regular file."

def test_benchmark_results():
    file_path = "/home/user/benchmark_results.json"
    assert os.path.exists(file_path), f"Missing required file: {file_path}"

    with open(file_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} is not valid JSON")

    assert isinstance(results, dict), f"Expected {file_path} to contain a JSON object"
    expected_keys = {"naive_time_sec", "grid_time_sec", "speedup"}
    assert expected_keys.issubset(results.keys()), f"Missing keys in benchmark_results.json. Expected {expected_keys}"

    for key in expected_keys:
        assert isinstance(results[key], (int, float)), f"Expected {key} to be a number, got {type(results[key])}"

def test_query_results_correctness():
    zones_path = "/home/user/delivery_zones.json"
    queries_path = "/home/user/queries.json"
    results_path = "/home/user/query_results.json"

    assert os.path.exists(results_path), f"Missing required file: {results_path}"

    with open(zones_path, "r") as f:
        zones = json.load(f)

    with open(queries_path, "r") as f:
        queries = json.load(f)

    expected_results = []
    for q in queries:
        qx, qy, r = q["qx"], q["qy"], q["radius"]
        min_cost = float('inf')
        found = False
        for z in zones:
            dist = math.sqrt((z["x"] - qx)**2 + (z["y"] - qy)**2)
            if dist <= r:
                cost = z["base_cost"] + (z["multiplier"] * dist)
                if cost < min_cost:
                    min_cost = cost
                    found = True

        if found:
            expected_results.append(round(min_cost, 2))
        else:
            expected_results.append(-1.0)

    with open(results_path, "r") as f:
        try:
            actual_results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} is not valid JSON")

    assert isinstance(actual_results, list), f"Expected {results_path} to contain a JSON array"
    assert len(actual_results) == len(expected_results), f"Expected {len(expected_results)} results, got {len(actual_results)}"

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        assert math.isclose(actual, expected, rel_tol=1e-5, abs_tol=1e-2), f"Result at index {i} is incorrect. Expected {expected}, got {actual}"
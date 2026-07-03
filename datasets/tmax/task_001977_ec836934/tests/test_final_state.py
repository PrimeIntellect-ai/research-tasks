# test_final_state.py

import os
import json
import math
import pytest

def test_analysis_results_exists():
    """Test that the analysis_results.json file exists."""
    file_path = '/home/user/analysis_results.json'
    assert os.path.isfile(file_path), f"File not found: {file_path}"

def test_analysis_results_format_and_values():
    """Test the structure and values of the analysis_results.json file."""
    file_path = '/home/user/analysis_results.json'
    with open(file_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("analysis_results.json is not a valid JSON file.")

    assert "max_stability_diff" in results, "Missing key: max_stability_diff"
    assert "wasserstein_distance" in results, "Missing key: wasserstein_distance"

    max_diff = results["max_stability_diff"]
    w_dist = results["wasserstein_distance"]

    assert isinstance(max_diff, (int, float)), "max_stability_diff must be a float"
    assert isinstance(w_dist, (int, float)), "wasserstein_distance must be a float"

    # Recompute Wasserstein distance using standard library
    # Read and parse the raw observations
    raw_file = '/home/user/raw_observations.txt'
    assert os.path.isfile(raw_file), "raw_observations.txt is missing"

    data = []
    with open(raw_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            t_val = float(parts[0].split('time_point:')[1])
            c_val = float(parts[1].split('concentration:')[1])
            data.append((t_val, c_val))

    # Sort chronologically
    data.sort(key=lambda x: x[0])
    t_eval = [x[0] for x in data]
    obs_vals = [x[1] for x in data]

    # The exact ODE solution for C' = -0.6 * C, C(0) = 1.0 is C(t) = exp(-0.6 * t)
    # Run B is highly accurate, so it closely approximates the exact solution
    exact_vals = [math.exp(-0.6 * t) for t in t_eval]

    # 1D Wasserstein distance for uniformly weighted samples of equal size
    # is the mean absolute difference of the sorted arrays
    sorted_obs = sorted(obs_vals)
    sorted_exact = sorted(exact_vals)

    expected_w_dist = sum(abs(a - b) for a, b in zip(sorted_obs, sorted_exact)) / len(sorted_obs)

    # Allow some tolerance because Run B is a numerical approximation (atol=1e-9, rtol=1e-9)
    assert math.isclose(w_dist, expected_w_dist, rel_tol=1e-3, abs_tol=1e-5), \
        f"wasserstein_distance is incorrect. Expected ~{expected_w_dist}, got {w_dist}"

    # The max stability diff should be a small positive float (typically > 0 due to numerical differences, but very small)
    assert 0.0 <= max_diff < 1e-2, f"max_stability_diff {max_diff} is out of expected plausible range."
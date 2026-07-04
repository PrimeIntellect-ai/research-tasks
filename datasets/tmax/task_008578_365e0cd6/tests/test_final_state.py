# test_final_state.py

import os
import json
import math

def test_latency_plot_exists_and_is_png():
    """Verify that the latency plot was created and is a valid PNG file."""
    plot_path = '/home/user/latency_plot.png'
    assert os.path.exists(plot_path), f"Plot file not found at {plot_path}"
    assert os.path.isfile(plot_path), f"Path {plot_path} is not a file"

    with open(plot_path, 'rb') as f:
        header = f.read(8)
    # PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
    assert header == b'\x89PNG\r\n\x1a\n', f"File {plot_path} is not a valid PNG image"

def test_analysis_results_json():
    """Verify that the analysis results JSON exists and contains the correct values."""
    json_path = '/home/user/analysis_results.json'
    assert os.path.exists(json_path), f"JSON log file not found at {json_path}"
    assert os.path.isfile(json_path), f"Path {json_path} is not a file"

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON"

    # Check structure
    assert "algo_A" in results, "Missing 'algo_A' in JSON"
    assert "algo_B" in results, "Missing 'algo_B' in JSON"
    assert "mann_whitney_p_value" in results, "Missing 'mann_whitney_p_value' in JSON"

    for algo in ["algo_A", "algo_B"]:
        for key in ["95th_percentile", "ci_lower", "ci_upper"]:
            assert key in results[algo], f"Missing '{key}' in '{algo}'"

    # Validate values with tolerances
    # Expected values from the ground truth
    exp_p95_A = 239.389
    exp_ci_lower_A = 231.144
    exp_ci_upper_A = 247.962

    exp_p95_B = 213.916
    exp_ci_lower_B = 206.940
    exp_ci_upper_B = 221.758

    # Algo A
    assert math.isclose(results["algo_A"]["95th_percentile"], exp_p95_A, abs_tol=0.5), \
        f"algo_A 95th_percentile {results['algo_A']['95th_percentile']} not within expected range of {exp_p95_A}"
    assert math.isclose(results["algo_A"]["ci_lower"], exp_ci_lower_A, abs_tol=1.0), \
        f"algo_A ci_lower {results['algo_A']['ci_lower']} not within expected range of {exp_ci_lower_A}"
    assert math.isclose(results["algo_A"]["ci_upper"], exp_ci_upper_A, abs_tol=1.0), \
        f"algo_A ci_upper {results['algo_A']['ci_upper']} not within expected range of {exp_ci_upper_A}"

    # Algo B
    assert math.isclose(results["algo_B"]["95th_percentile"], exp_p95_B, abs_tol=0.5), \
        f"algo_B 95th_percentile {results['algo_B']['95th_percentile']} not within expected range of {exp_p95_B}"
    assert math.isclose(results["algo_B"]["ci_lower"], exp_ci_lower_B, abs_tol=1.0), \
        f"algo_B ci_lower {results['algo_B']['ci_lower']} not within expected range of {exp_ci_lower_B}"
    assert math.isclose(results["algo_B"]["ci_upper"], exp_ci_upper_B, abs_tol=1.0), \
        f"algo_B ci_upper {results['algo_B']['ci_upper']} not within expected range of {exp_ci_upper_B}"

    # Mann-Whitney P-value
    p_value = results["mann_whitney_p_value"]
    assert p_value < 0.001, f"mann_whitney_p_value {p_value} is not less than 0.001"
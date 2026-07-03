# test_final_state.py

import os
import json
import math
import pytest

def test_svg_plot_exists():
    svg_path = "/home/user/output/gc_plot.svg"
    assert os.path.isfile(svg_path), f"Plot file missing: {svg_path}"
    with open(svg_path, "r") as f:
        content = f.read()
    assert "<svg" in content.lower(), f"File {svg_path} does not appear to be a valid SVG"

def test_results_json():
    json_path = "/home/user/output/results.json"
    assert os.path.isfile(json_path), f"Results file missing: {json_path}"

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON")

    expected_keys = {
        "total_gc_integral",
        "regression_slope",
        "regression_intercept",
        "bootstrap_ci_lower",
        "bootstrap_ci_upper"
    }
    for key in expected_keys:
        assert key in results, f"Missing key '{key}' in {json_path}"
        assert isinstance(results[key], (int, float)), f"Value for '{key}' must be a number"

    # Read the fasta file to compute the exact expected values
    fasta_path = "/home/user/data/genome.fasta"
    assert os.path.isfile(fasta_path), "Fasta file missing, cannot validate results"

    seq = []
    with open(fasta_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith(">"):
                seq.append(line)
    full_seq = "".join(seq)

    # Calculate windowed GC ratios (window=100, step=100)
    window_size = 100
    gc_ratios = []
    for i in range(0, len(full_seq), window_size):
        chunk = full_seq[i:i+window_size]
        if len(chunk) == window_size:
            gc_count = chunk.count('G') + chunk.count('C')
            gc_ratios.append(gc_count / window_size)

    # 1. total_gc_integral
    expected_sum = sum(gc_ratios)
    assert math.isclose(results["total_gc_integral"], expected_sum, rel_tol=1e-9), \
        f"Expected total_gc_integral ~ {expected_sum}, got {results['total_gc_integral']}"

    # 2. Linear regression
    n = len(gc_ratios)
    x = list(range(n))
    mean_x = sum(x) / n
    mean_y = expected_sum / n

    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, gc_ratios))
    denominator = sum((xi - mean_x) ** 2 for xi in x)
    expected_slope = numerator / denominator
    expected_intercept = mean_y - expected_slope * mean_x

    assert math.isclose(results["regression_slope"], expected_slope, rel_tol=1e-5, abs_tol=1e-7), \
        f"Expected regression_slope ~ {expected_slope}, got {results['regression_slope']}"
    assert math.isclose(results["regression_intercept"], expected_intercept, rel_tol=1e-5, abs_tol=1e-7), \
        f"Expected regression_intercept ~ {expected_intercept}, got {results['regression_intercept']}"

    # 3. Bootstrap CI sanity checks
    ci_lower = results["bootstrap_ci_lower"]
    ci_upper = results["bootstrap_ci_upper"]
    assert ci_lower < mean_y < ci_upper, \
        f"Confidence interval [{ci_lower}, {ci_upper}] does not contain the sample mean {mean_y}"
    assert ci_upper - ci_lower > 0, "Confidence interval has zero or negative width"
    assert ci_upper - ci_lower < 0.05, "Confidence interval is unusually wide for n=1000"
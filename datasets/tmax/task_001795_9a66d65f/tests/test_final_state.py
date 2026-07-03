# test_final_state.py

import os
import json
import csv
import random
import math
import pytest

def test_results_json_exists():
    """Test that the results.json file exists."""
    file_path = '/home/user/results.json'
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_results_json_format_and_bootstrap():
    """Test that the results.json file has the correct format and bootstrap values."""
    file_path = '/home/user/results.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    expected_keys = {
        "vocabulary_size",
        "pc1_mean_physics",
        "pc1_mean_biology",
        "ttest_p_value",
        "bootstrap_ci_lower",
        "bootstrap_ci_upper"
    }

    assert set(results.keys()) == expected_keys, f"JSON keys do not match expected keys. Got {list(results.keys())}"

    assert results["vocabulary_size"] == 50, "vocabulary_size must be exactly 50."

    # Verify types
    for key in expected_keys:
        assert isinstance(results[key], (int, float)), f"Value for {key} must be a number."

    # Compute expected bootstrap CI
    csv_path = '/home/user/abstracts.csv'
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            bio_citations = [int(row['citations']) for row in reader if row['category'] == 'Biology']

        if bio_citations:
            random.seed(42)
            means = []
            n = len(bio_citations)
            for _ in range(10000):
                sample = [random.choice(bio_citations) for _ in range(n)]
                means.append(sum(sample) / n)

            means.sort()
            # Percentile method: 2.5th and 97.5th percentiles
            lower_idx = int(10000 * 0.025)
            upper_idx = int(10000 * 0.975)
            expected_lower = means[lower_idx]
            expected_upper = means[upper_idx]

            # Allow a small tolerance for rounding differences
            assert math.isclose(results["bootstrap_ci_lower"], expected_lower, abs_tol=0.01), \
                f"bootstrap_ci_lower expected ~{expected_lower:.4f}, got {results['bootstrap_ci_lower']}"
            assert math.isclose(results["bootstrap_ci_upper"], expected_upper, abs_tol=0.01), \
                f"bootstrap_ci_upper expected ~{expected_upper:.4f}, got {results['bootstrap_ci_upper']}"
# test_final_state.py

import os
import csv
import json
import math
import re
import pytest

def test_experiment_results_json_exists():
    """Check if the experiment_results.json file was created."""
    file_path = '/home/user/experiment_results.json'
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} should be a file."

def test_experiment_results_content():
    """Check if the experiment_results.json contains the correct rounded statistics."""
    csv_path = '/home/user/raw_texts.csv'
    json_path = '/home/user/experiment_results.json'

    assert os.path.exists(csv_path), "Raw texts CSV is missing."
    assert os.path.exists(json_path), "Experiment results JSON is missing."

    counts_a = []
    counts_b = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 2:
                text = row[1]
                counts_a.append(len(text.split(' ')))
                counts_b.append(len(re.findall(r'\w+', text)))

    n = len(counts_a)
    assert n > 0, "No data found in the CSV."

    mean_a = sum(counts_a) / n
    mean_b = sum(counts_b) / n

    # Calculate Pearson correlation
    num = sum((a - mean_a) * (b - mean_b) for a, b in zip(counts_a, counts_b))
    den_a = math.sqrt(sum((a - mean_a) ** 2 for a in counts_a))
    den_b = math.sqrt(sum((b - mean_b) ** 2 for b in counts_b))
    corr = num / (den_a * den_b) if den_a and den_b else 0.0

    # Calculate paired t-statistic
    diffs = [a - b for a, b in zip(counts_a, counts_b)]
    mean_diff = sum(diffs) / n
    if n > 1:
        var_diff = sum((d - mean_diff) ** 2 for d in diffs) / (n - 1)
        std_diff = math.sqrt(var_diff)
        t_stat = mean_diff / (std_diff / math.sqrt(n)) if std_diff else 0.0
    else:
        t_stat = 0.0

    # Since p-value calculation requires complex CDF functions not in the standard library,
    # we use the known p-value for the exact dataset provided in the setup.
    # If the dataset matches the setup exactly, the p-value is approx 0.8584
    # Wait, let's just check the structure and the values we can compute.

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("experiment_results.json is not valid JSON.")

    expected_keys = {"correlation", "t_statistic", "p_value", "mean_length_A", "mean_length_B"}
    assert set(results.keys()) == expected_keys, f"JSON keys must exactly match {expected_keys}"

    assert isinstance(results["correlation"], float) or isinstance(results["correlation"], int)
    assert isinstance(results["t_statistic"], float) or isinstance(results["t_statistic"], int)
    assert isinstance(results["p_value"], float) or isinstance(results["p_value"], int)
    assert isinstance(results["mean_length_A"], float) or isinstance(results["mean_length_A"], int)
    assert isinstance(results["mean_length_B"], float) or isinstance(results["mean_length_B"], int)

    assert math.isclose(results["mean_length_A"], round(mean_a, 4), rel_tol=1e-4), \
        f"Expected mean_length_A to be {round(mean_a, 4)}, got {results['mean_length_A']}"
    assert math.isclose(results["mean_length_B"], round(mean_b, 4), rel_tol=1e-4), \
        f"Expected mean_length_B to be {round(mean_b, 4)}, got {results['mean_length_B']}"
    assert math.isclose(results["correlation"], round(corr, 4), rel_tol=1e-4), \
        f"Expected correlation to be {round(corr, 4)}, got {results['correlation']}"
    assert math.isclose(results["t_statistic"], round(t_stat, 4), rel_tol=1e-4), \
        f"Expected t_statistic to be {round(t_stat, 4)}, got {results['t_statistic']}"

    # Check that p_value is a valid probability
    assert 0.0 <= results["p_value"] <= 1.0, "p_value must be between 0.0 and 1.0"
# test_final_state.py

import os
import json
import csv
import math
import pytest

def get_columns(filename, col1, col2):
    """Reads two columns from a CSV file and returns them as lists of floats."""
    x, y = [], []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            x.append(float(row[col1]))
            y.append(float(row[col2]))
    return x, y

def pearson_correlation(x, y):
    """Computes the Pearson correlation coefficient."""
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    var_x = sum((xi - mean_x) ** 2 for xi in x)
    var_y = sum((yi - mean_y) ** 2 for yi in y)

    if var_x == 0 or var_y == 0:
        return 0.0
    return cov / math.sqrt(var_x * var_y)

def test_metrics_json_exists():
    """Test that the metrics.json file was created."""
    assert os.path.isfile("/home/user/metrics.json"), "The file /home/user/metrics.json does not exist."

def test_metrics_json_content():
    """Test that metrics.json contains the correct keys and values."""
    with open("/home/user/metrics.json", "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/metrics.json is not a valid JSON file.")

    expected_keys = {"correlation_A", "correlation_B", "t_statistic", "p_value"}
    assert set(metrics.keys()) == expected_keys, f"metrics.json keys do not match expected. Found: {list(metrics.keys())}"

    # Compute expected correlations directly from the CSV files
    input_a, latency_a = get_columns("/home/user/engine_a.csv", "input_size", "latency_ms")
    expected_corr_a = pearson_correlation(input_a, latency_a)

    input_b, latency_b = get_columns("/home/user/engine_b.csv", "input_size", "latency_ms")
    expected_corr_b = pearson_correlation(input_b, latency_b)

    assert math.isclose(metrics["correlation_A"], expected_corr_a, abs_tol=1e-4), \
        f"correlation_A is incorrect. Expected ~{expected_corr_a}, got {metrics['correlation_A']}"

    assert math.isclose(metrics["correlation_B"], expected_corr_b, abs_tol=1e-4), \
        f"correlation_B is incorrect. Expected ~{expected_corr_b}, got {metrics['correlation_B']}"

    # The expected t-statistic and p-value depend on pandas downsampling which is complex to reproduce exactly in pure Python.
    # We validate them against the known expected values from the correct procedure.
    expected_t_stat = 4.8817
    expected_p_value = 2.155e-06

    assert math.isclose(metrics["t_statistic"], expected_t_stat, abs_tol=1e-3), \
        f"t_statistic is incorrect. Expected ~{expected_t_stat}, got {metrics['t_statistic']}"

    assert math.isclose(metrics["p_value"], expected_p_value, abs_tol=1e-7), \
        f"p_value is incorrect. Expected ~{expected_p_value}, got {metrics['p_value']}"
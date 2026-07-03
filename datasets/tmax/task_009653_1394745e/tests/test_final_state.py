# test_final_state.py
import os
import json
import csv
import re
import math
import statistics
import pytest

def test_analysis_report_exists():
    """Check if the analysis report was created."""
    assert os.path.isfile("/home/user/analysis_report.json"), "analysis_report.json is missing."

def test_analysis_report_contents():
    """Validate the contents of the analysis report."""
    report_path = "/home/user/analysis_report.json"
    assert os.path.isfile(report_path), "analysis_report.json is missing."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("analysis_report.json is not a valid JSON file.")

    expected_keys = {
        "median_latency_imputed",
        "cpu_outliers_capped",
        "vocab_size",
        "t_stat",
        "p_value",
        "ci_lower",
        "ci_upper"
    }

    missing_keys = expected_keys - set(report.keys())
    assert not missing_keys, f"Missing keys in JSON: {missing_keys}"

    # Read CSV to compute expected values
    csv_path = "/home/user/server_logs.csv"
    assert os.path.isfile(csv_path), "server_logs.csv is missing."

    latencies = []
    cpu_usages = []
    messages = []

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lat_str = row["latency_ms"]
            if lat_str and lat_str.lower() != "nan":
                latencies.append(float(lat_str))
            else:
                latencies.append(None)

            cpu_usages.append(float(row["cpu_usage"]))
            messages.append(row["log_message"])

    # 1. Median Imputation
    valid_latencies = [x for x in latencies if x is not None]
    median_lat = statistics.median(valid_latencies)

    imputed_latencies = [x if x is not None else median_lat for x in latencies]

    # 2. Outliers
    mean_cpu = statistics.mean(cpu_usages)
    std_cpu = statistics.stdev(cpu_usages)
    upper = mean_cpu + 3 * std_cpu
    lower = mean_cpu - 3 * std_cpu

    cpu_outliers_capped = sum(1 for x in cpu_usages if x > upper or x < lower)

    # 3. Tokenization
    vocab = set()
    tokens_list = []
    for msg in messages:
        msg_lower = msg.lower()
        msg_clean = re.sub(r'[^a-z0-9\s]', '', msg_lower)
        tokens = msg_clean.split()
        tokens_list.append(tokens)
        vocab.update(tokens)

    vocab_size = len(vocab)

    # 4. Hypothesis Testing (t-stat)
    group_a = []
    group_b = []
    for tokens, lat in zip(tokens_list, imputed_latencies):
        if "timeout" in tokens:
            group_a.append(lat)
        else:
            group_b.append(lat)

    mean_a = statistics.mean(group_a)
    mean_b = statistics.mean(group_b)
    var_a = statistics.variance(group_a)
    var_b = statistics.variance(group_b)
    n_a = len(group_a)
    n_b = len(group_b)

    se = math.sqrt(var_a/n_a + var_b/n_b)
    t_stat = (mean_a - mean_b) / se

    # Validate easy-to-compute values
    assert math.isclose(report["median_latency_imputed"], median_lat, abs_tol=1e-3), \
        f"Expected median_latency_imputed approx {median_lat}, got {report['median_latency_imputed']}"

    assert report["cpu_outliers_capped"] == cpu_outliers_capped, \
        f"Expected cpu_outliers_capped {cpu_outliers_capped}, got {report['cpu_outliers_capped']}"

    assert report["vocab_size"] == vocab_size, \
        f"Expected vocab_size {vocab_size}, got {report['vocab_size']}"

    assert math.isclose(report["t_stat"], t_stat, abs_tol=1e-3), \
        f"Expected t_stat approx {t_stat}, got {report['t_stat']}"

    # For p_value and CI, since we can't easily compute t-distribution CDF/PPF in pure Python,
    # we just ensure they are floats and logically sound (e.g. p-value between 0 and 1)
    assert isinstance(report["p_value"], (int, float)), "p_value must be a number"
    assert 0.0 <= report["p_value"] <= 1.0, "p_value must be between 0 and 1"

    assert isinstance(report["ci_lower"], (int, float)), "ci_lower must be a number"
    assert isinstance(report["ci_upper"], (int, float)), "ci_upper must be a number"
    assert report["ci_lower"] < report["ci_upper"], "ci_lower must be less than ci_upper"
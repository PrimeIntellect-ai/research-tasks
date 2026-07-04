# test_final_state.py

import os
import json
import pytest
import numpy as np
import pandas as pd
from scipy.stats import wasserstein_distance

def test_perf_report_json_exists():
    path = "/home/user/perf_report.json"
    assert os.path.isfile(path), f"Missing output file: {path}"

def test_metrics_accuracy():
    report_path = "/home/user/perf_report.json"
    baseline_path = "/home/user/baseline_perf.csv"
    optimized_path = "/home/user/optimized_perf.csv"

    assert os.path.isfile(report_path), f"Missing {report_path}"
    assert os.path.isfile(baseline_path), f"Missing {baseline_path}"
    assert os.path.isfile(optimized_path), f"Missing {optimized_path}"

    with open(report_path, "r", encoding="utf-8") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "wasserstein_distance" in report, "Missing 'wasserstein_distance' in report."
    assert "mean_diff_ci_lower" in report, "Missing 'mean_diff_ci_lower' in report."
    assert "mean_diff_ci_upper" in report, "Missing 'mean_diff_ci_upper' in report."

    # Load data
    baseline_df = pd.read_csv(baseline_path, header=None)
    optimized_df = pd.read_csv(optimized_path, header=None)

    baseline = baseline_df.values.flatten()
    optimized = optimized_df.values.flatten()

    # Compute Wasserstein distance
    true_wd = wasserstein_distance(baseline, optimized)
    student_wd = float(report["wasserstein_distance"])
    wd_error = abs(true_wd - student_wd)
    assert wd_error < 0.05, f"Wasserstein distance error too high: expected ~{true_wd:.4f}, got {student_wd:.4f} (error: {wd_error:.4f} >= 0.05)"

    # Compute reference bootstrap CI
    np.random.seed(42)
    n_resamples = 1000
    n_b = len(baseline)
    n_o = len(optimized)

    diffs = []
    for _ in range(n_resamples):
        b_resample = np.random.choice(baseline, size=n_b, replace=True)
        o_resample = np.random.choice(optimized, size=n_o, replace=True)
        diffs.append(np.mean(b_resample) - np.mean(o_resample))

    true_ci_lower = np.percentile(diffs, 2.5)
    true_ci_upper = np.percentile(diffs, 97.5)

    student_ci_lower = float(report["mean_diff_ci_lower"])
    student_ci_upper = float(report["mean_diff_ci_upper"])

    lower_error = abs(true_ci_lower - student_ci_lower)
    upper_error = abs(true_ci_upper - student_ci_upper)

    assert lower_error < 0.5, f"CI lower bound error too high: expected ~{true_ci_lower:.4f}, got {student_ci_lower:.4f} (error: {lower_error:.4f} >= 0.5)"
    assert upper_error < 0.5, f"CI upper bound error too high: expected ~{true_ci_upper:.4f}, got {student_ci_upper:.4f} (error: {upper_error:.4f} >= 0.5)"
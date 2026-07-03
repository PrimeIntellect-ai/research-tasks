# test_final_state.py

import os
import json
import csv
import math
import statistics
import pytest

RAW_DATA_PATH = "/home/user/raw_profiling.txt"
CSV_PATH = "/home/user/reshaped_data.csv"
JSON_PATH = "/home/user/profiling_report.json"

def compute_expected_data():
    """Reads raw data and computes expected CSV rows and t-test statistics."""
    expected_csv = []
    algo_a_times = []
    algo_b_times = []

    with open(RAW_DATA_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            run_id, algo, target, primer, time_ns = parts
            time_ns = float(time_ns)

            # Compute match score
            match_score = sum(1 for t, p in zip(target, primer) if t == p)
            expected_csv.append((run_id, algo, str(match_score), str(int(time_ns))))

            if algo == "AlgoA":
                algo_a_times.append(time_ns)
            elif algo == "AlgoB":
                algo_b_times.append(time_ns)

    # Compute Welch's t-test stats
    n_a = len(algo_a_times)
    n_b = len(algo_b_times)

    mean_a = statistics.mean(algo_a_times)
    mean_b = statistics.mean(algo_b_times)

    var_a = statistics.variance(algo_a_times)
    var_b = statistics.variance(algo_b_times)

    se_a = var_a / n_a
    se_b = var_b / n_b

    t_stat = (mean_a - mean_b) / math.sqrt(se_a + se_b)

    df_num = (se_a + se_b) ** 2
    df_den = (se_a ** 2 / (n_a - 1)) + (se_b ** 2 / (n_b - 1))
    df = df_num / df_den

    return expected_csv, mean_a, mean_b, t_stat, df

def test_reshaped_data_csv():
    """Validates the reshaped CSV file contents."""
    assert os.path.isfile(CSV_PATH), f"Reshaped CSV file not found at {CSV_PATH}"

    expected_csv, _, _, _, _ = compute_expected_data()

    with open(CSV_PATH, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."

    header = rows[0]
    expected_header = ["run_id", "algorithm", "match_score", "time_ns"]
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_csv), f"Expected {len(expected_csv)} data rows, got {len(data_rows)}"

    # Sort both to ensure order doesn't cause false failures, though order should ideally match
    expected_csv_sorted = sorted(expected_csv, key=lambda x: x[0])
    data_rows_sorted = sorted(data_rows, key=lambda x: x[0])

    for expected, actual in zip(expected_csv_sorted, data_rows_sorted):
        assert actual == list(expected), f"CSV row mismatch. Expected {expected}, got {actual}"

def test_profiling_report_json():
    """Validates the profiling report JSON file contents."""
    assert os.path.isfile(JSON_PATH), f"Profiling report JSON not found at {JSON_PATH}"

    with open(JSON_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {JSON_PATH} is not valid JSON.")

    expected_keys = {"algo_a_mean", "algo_b_mean", "t_statistic", "degrees_of_freedom", "p_value", "significant_at_05"}
    assert set(report.keys()) == expected_keys, f"JSON keys mismatch. Expected {expected_keys}, got {set(report.keys())}"

    _, mean_a, mean_b, t_stat, df = compute_expected_data()

    assert math.isclose(report["algo_a_mean"], mean_a, rel_tol=1e-3), f"algo_a_mean mismatch. Expected ~{mean_a}, got {report['algo_a_mean']}"
    assert math.isclose(report["algo_b_mean"], mean_b, rel_tol=1e-3), f"algo_b_mean mismatch. Expected ~{mean_b}, got {report['algo_b_mean']}"

    # The t-statistic could be negative depending on order, but Welch's formula above used (A - B)
    assert math.isclose(abs(report["t_statistic"]), abs(t_stat), rel_tol=1e-3), f"t_statistic mismatch. Expected ~{t_stat}, got {report['t_statistic']}"
    assert math.isclose(report["degrees_of_freedom"], df, rel_tol=1e-3), f"degrees_of_freedom mismatch. Expected ~{df}, got {report['degrees_of_freedom']}"

    # P-value should be around 0.0151
    p_value = report["p_value"]
    assert 0.01 < p_value < 0.02, f"p_value out of expected range (0.01 - 0.02). Got {p_value}"

    assert report["significant_at_05"] is True, "significant_at_05 should be true since p_value < 0.05"
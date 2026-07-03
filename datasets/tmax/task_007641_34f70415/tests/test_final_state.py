# test_final_state.py
import os
import json
import csv
import math
import stat
import pytest

def get_percentile(data, percentile):
    n = len(data)
    if n == 0:
        return None
    data = sorted(data)
    k = (n - 1) * (percentile / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return data[int(k)]
    d0 = data[int(f)]
    d1 = data[int(c)]
    return d0 + (d1 - d0) * (k - f)

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Expected script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_report_json_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Expected report {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    required_keys = {
        "model_A_cleaned_count",
        "model_B_cleaned_count",
        "mean_diff_observed",
        "ci_lower",
        "ci_upper"
    }
    assert set(data.keys()) == required_keys, f"JSON must contain exactly the keys: {required_keys}"

def test_report_values():
    # Recompute deterministic parts using stdlib
    csv_path = "/home/user/inference_logs.csv"
    assert os.path.isfile(csv_path), f"Data file {csv_path} is missing."

    latencies = {'A': [], 'B': []}
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = row['latency']
            if val == 'NA' or val == '':
                continue
            try:
                v = float(val)
                if v >= 0:
                    latencies[row['model']].append(v)
            except ValueError:
                continue

    cleaned = {}
    for model in ['A', 'B']:
        data = latencies[model]
        q1 = get_percentile(data, 25)
        q3 = get_percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        cleaned[model] = [x for x in data if lower_bound <= x <= upper_bound]

    count_A = len(cleaned['A'])
    count_B = len(cleaned['B'])
    mean_A = sum(cleaned['A']) / count_A
    mean_B = sum(cleaned['B']) / count_B
    mean_diff = mean_B - mean_A

    # Read student report
    report_path = "/home/user/report.json"
    with open(report_path, "r") as f:
        data = json.load(f)

    assert data["model_A_cleaned_count"] == count_A, f"Expected model_A_cleaned_count to be {count_A}, got {data['model_A_cleaned_count']}"
    assert data["model_B_cleaned_count"] == count_B, f"Expected model_B_cleaned_count to be {count_B}, got {data['model_B_cleaned_count']}"

    assert abs(data["mean_diff_observed"] - mean_diff) <= 0.02, \
        f"Expected mean_diff_observed to be approx {mean_diff:.2f}, got {data['mean_diff_observed']}"

    # Bootstrap CI relies on numpy's specific random generator, so we check against the known truth values
    expected_ci_lower = 5.92
    expected_ci_upper = 8.87

    assert abs(data["ci_lower"] - expected_ci_lower) <= 0.05, \
        f"Expected ci_lower to be approx {expected_ci_lower}, got {data['ci_lower']}"
    assert abs(data["ci_upper"] - expected_ci_upper) <= 0.05, \
        f"Expected ci_upper to be approx {expected_ci_upper}, got {data['ci_upper']}"
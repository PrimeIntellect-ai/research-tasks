# test_final_state.py

import os
import json
import csv
import math
import pytest

def get_clean_data(file_path):
    latencies = []
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            val = row['latency_ms']
            if not val or val.lower() == 'nan':
                continue
            try:
                latencies.append(float(val))
            except ValueError:
                pass

    if not latencies:
        return []

    # Calculate P99 using linear interpolation (pandas default)
    sorted_lats = sorted(latencies)
    n = len(sorted_lats)
    idx = (n - 1) * 0.99
    lower = int(math.floor(idx))
    upper = int(math.ceil(idx))
    weight = idx - lower

    if lower == upper:
        p99 = sorted_lats[lower]
    else:
        p99 = sorted_lats[lower] * (1 - weight) + sorted_lats[upper] * weight

    # Filter valid latencies
    return [x for x in latencies if 0 <= x <= p99]

def compute_t_stat(v1, v2):
    n1, n2 = len(v1), len(v2)
    mean1 = sum(v1) / n1
    mean2 = sum(v2) / n2

    var1 = sum((x - mean1)**2 for x in v1) / (n1 - 1)
    var2 = sum((x - mean2)**2 for x in v2) / (n2 - 1)

    se1_sq = var1 / n1
    se2_sq = var2 / n2

    t_stat = (mean1 - mean2) / math.sqrt(se1_sq + se2_sq)
    return t_stat

def test_report_json_exists_and_format():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Expected output file {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected_keys = {"t_stat", "p_value", "ci_lower", "ci_upper"}
    assert set(data.keys()) == expected_keys, f"JSON keys do not match. Expected {expected_keys}, got {set(data.keys())}"

    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"Value for {key} must be a number."

def test_report_json_values():
    report_path = "/home/user/report.json"
    if not os.path.isfile(report_path):
        pytest.skip("Report file missing.")

    with open(report_path, 'r') as f:
        data = json.load(f)

    v1_clean = get_clean_data('/home/user/model_v1.csv')
    v2_clean = get_clean_data('/home/user/model_v2.csv')

    assert len(v1_clean) > 0, "No valid data found for model_v1 after cleaning."
    assert len(v2_clean) > 0, "No valid data found for model_v2 after cleaning."

    expected_t_stat = compute_t_stat(v1_clean, v2_clean)

    assert math.isclose(data['t_stat'], expected_t_stat, abs_tol=1e-3), \
        f"t_stat mismatch: expected {expected_t_stat:.4f}, got {data['t_stat']}"

    # We ensure the confidence interval makes logical sense
    assert data['ci_lower'] < data['ci_upper'], "ci_lower must be less than ci_upper"
    assert 0 <= data['p_value'] <= 1, "p_value must be between 0 and 1"
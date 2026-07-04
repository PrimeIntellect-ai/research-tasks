# test_final_state.py
import csv
import json
import math
import os
import pytest

def get_expected_state():
    """
    Computes the expected state directly from the initial sensor_data.csv
    using only the Python standard library.
    """
    input_file = '/home/user/sensor_data.csv'
    if not os.path.exists(input_file):
        pytest.fail(f"Input file {input_file} is missing, cannot compute expected state.")

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = []
        for row in reader:
            try:
                floats = [float(x) for x in row]
                # Drop rows with out-of-bounds values
                if all(-100.0 <= x <= 100.0 for x in floats):
                    data.append(floats)
            except ValueError:
                pass

    # Calculate correlations
    cols = list(zip(*data))
    n = len(data)
    means = [sum(c)/n for c in cols]
    stdevs = [math.sqrt(sum((x - m)**2 for x in c)) for c, m in zip(cols, means)]

    corrs = {}
    for i in range(len(header)):
        for j in range(i+1, len(header)):
            cov = sum((cols[i][k] - means[i]) * (cols[j][k] - means[j]) for k in range(n))
            corr = cov / (stdevs[i] * stdevs[j]) if stdevs[i] and stdevs[j] else 0
            corrs[(header[i], header[j])] = corr

    # Identify dropped columns
    to_drop = set()
    sorted_headers = sorted(header)
    for i in range(len(sorted_headers)):
        for j in range(i+1, len(sorted_headers)):
            h1, h2 = sorted_headers[i], sorted_headers[j]
            idx1, idx2 = header.index(h1), header.index(h2)
            key = (header[idx1], header[idx2]) if idx1 < idx2 else (header[idx2], header[idx1])
            if abs(corrs[key]) > 0.90:
                to_drop.add(h2)

    retained_headers = [h for h in header if h not in to_drop]
    retained_indices = [header.index(h) for h in retained_headers]

    # Bayesian Anomaly Detection
    total_anomalies = 0
    anomalies_by_col = {h: [] for h in retained_headers}

    def norm_pdf(x):
        return math.exp(-0.5 * (x / 10.0)**2) / (10.0 * math.sqrt(2 * math.pi))

    for row in data:
        for idx, h in zip(retained_indices, retained_headers):
            val = row[idx]
            p_n = norm_pdf(val)
            p_f = 0.005
            post_f = (p_f * 0.05) / (p_f * 0.05 + p_n * 0.95)
            flag = 1 if post_f > 0.5 else 0
            anomalies_by_col[h].append(flag)
            total_anomalies += flag

    return {
        'retained_headers': retained_headers,
        'dropped_columns': sorted(list(to_drop)),
        'total_anomalies': total_anomalies,
        'data_len': n,
        'anomalies_by_col': anomalies_by_col
    }

@pytest.fixture(scope="module")
def expected_state():
    return get_expected_state()

def test_report_json(expected_state):
    report_path = '/home/user/report.json'
    assert os.path.exists(report_path), f"Expected report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "dropped_columns" in report, "Report JSON missing 'dropped_columns' key."
    assert "total_anomalies" in report, "Report JSON missing 'total_anomalies' key."

    assert sorted(report["dropped_columns"]) == expected_state["dropped_columns"], \
        f"Expected dropped columns {expected_state['dropped_columns']}, but got {report['dropped_columns']}."

    assert report["total_anomalies"] == expected_state["total_anomalies"], \
        f"Expected total anomalies {expected_state['total_anomalies']}, but got {report['total_anomalies']}."

def test_cleaned_data_csv(expected_state):
    csv_path = '/home/user/cleaned_data.csv'
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail(f"File {csv_path} is empty.")

        expected_headers = expected_state["retained_headers"] + [f"failure_flag_{h}" for h in expected_state["retained_headers"]]

        # Check headers (order might vary, but standard is retained sensors then flags)
        assert set(header) == set(expected_headers), \
            f"Expected headers {set(expected_headers)}, but got {set(header)}."

        # Read data
        data = list(reader)

    assert len(data) == expected_state["data_len"], \
        f"Expected {expected_state['data_len']} rows after dropping out-of-bounds values, but got {len(data)} rows."

    # Verify anomaly flags for the first few rows to ensure correctness
    flag_indices = {h: header.index(f"failure_flag_{h}") for h in expected_state["retained_headers"]}

    for i, row in enumerate(data):
        for h in expected_state["retained_headers"]:
            expected_flag = expected_state["anomalies_by_col"][h][i]
            actual_flag = int(float(row[flag_indices[h]]))
            assert actual_flag == expected_flag, \
                f"Row {i+1}, column failure_flag_{h}: expected {expected_flag}, got {actual_flag}."
# test_final_state.py

import os
import csv
import math
import stat
import pytest

def test_pipeline_script_exists_and_executable():
    """Check if run_pipeline.sh exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def parse_and_clean_data(raw_path):
    """Helper to compute expected clean data based on task rules."""
    expected_clean = []
    with open(raw_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        expected_clean.append(header)
        for row in reader:
            if len(row) != 4:
                continue
            ts, sid, temp, hum = row
            try:
                sid = int(sid)
                temp = float(temp)
                hum = float(hum)
            except ValueError:
                continue

            if not (-50.0 <= temp <= 50.0):
                continue
            if not (0.0 <= hum <= 100.0):
                continue

            expected_clean.append(row)
    return expected_clean

def test_clean_data_correctness():
    """Validate clean_data.csv against expected task logic."""
    raw_path = "/home/user/raw_sensor_data.csv"
    clean_path = "/home/user/clean_data.csv"

    assert os.path.exists(clean_path), f"Missing output file: {clean_path}"

    expected_clean = parse_and_clean_data(raw_path)

    actual_clean = []
    with open(clean_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_clean.append(row)

    assert len(actual_clean) == len(expected_clean), f"Expected {len(expected_clean)} rows in clean_data.csv, got {len(actual_clean)}"
    assert actual_clean == expected_clean, "clean_data.csv content does not match expected cleaned data."

def compute_anomalies(clean_data):
    """Helper to compute expected anomalies based on Bayesian model rules."""
    header = clean_data[0]
    rows = clean_data[1:]

    # Group by sensor_id
    sensors = {}
    for row in rows:
        sid = int(row[1])
        temp = float(row[2])
        if sid not in sensors:
            sensors[sid] = []
        sensors[sid].append((temp, row))

    mu_0 = 20.0
    var_0 = 25.0
    var_like = 4.0

    expected_anomalies = [header]

    for sid, readings in sensors.items():
        n = len(readings)
        sum_x = sum(t for t, r in readings)

        # Posterior
        inv_var_post = (1.0 / var_0) + (n / var_like)
        var_post = 1.0 / inv_var_post
        mu_post = var_post * ((mu_0 / var_0) + (sum_x / var_like))

        # Predictive variance
        var_pred = var_post + var_like
        std_pred = math.sqrt(var_pred)

        threshold = 3.0 * std_pred

        for temp, row in readings:
            if abs(temp - mu_post) > threshold:
                expected_anomalies.append(row)

    return expected_anomalies

def test_anomalies_correctness():
    """Validate anomalies.csv against expected Bayesian anomaly logic."""
    raw_path = "/home/user/raw_sensor_data.csv"
    anomalies_path = "/home/user/anomalies.csv"

    assert os.path.exists(anomalies_path), f"Missing output file: {anomalies_path}"

    expected_clean = parse_and_clean_data(raw_path)
    expected_anomalies = compute_anomalies(expected_clean)

    actual_anomalies = []
    with open(anomalies_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_anomalies.append(row)

    assert len(actual_anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} rows in anomalies.csv, got {len(actual_anomalies)}"

    # Order might vary depending on implementation, so we check sets for the data rows
    expected_set = {tuple(r) for r in expected_anomalies[1:]}
    actual_set = {tuple(r) for r in actual_anomalies[1:]}

    assert actual_anomalies[0] == expected_anomalies[0], "Header mismatch in anomalies.csv"
    assert actual_set == expected_set, "Data rows in anomalies.csv do not match expected anomalies."

def test_benchmark_output():
    """Validate benchmark.txt exists and contains a parseable float."""
    benchmark_path = "/home/user/benchmark.txt"
    assert os.path.exists(benchmark_path), f"Missing output file: {benchmark_path}"

    with open(benchmark_path, 'r') as f:
        content = f.read().strip()

    assert content, "benchmark.txt is empty."

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse benchmark.txt content as float: '{content}'")

    assert val > 0.0, "Benchmark time should be strictly positive."
# test_final_state.py
import os
import struct
import math
import pytest

def test_c_source_exists():
    assert os.path.exists('/home/user/clean_data.c'), "C source file '/home/user/clean_data.c' is missing."

def test_executable_exists():
    assert os.path.exists('/home/user/clean_data'), "Compiled executable '/home/user/clean_data' is missing."

def test_anomalies_binary_exists():
    assert os.path.exists('/home/user/anomalies.bin'), "Anomalies binary '/home/user/anomalies.bin' is missing."

def test_report_exists():
    assert os.path.exists('/home/user/report.txt'), "Report file '/home/user/report.txt' is missing."

def test_mmap_used():
    source_path = '/home/user/clean_data.c'
    if os.path.exists(source_path):
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "mmap" in content, "The C program must use memory-mapped I/O (mmap) as per requirements."

def test_data_correctness():
    raw_data_path = '/home/user/raw_data.bin'
    anomalies_path = '/home/user/anomalies.bin'
    report_path = '/home/user/report.txt'

    # Ensure prerequisites exist before doing heavy computation
    if not os.path.exists(raw_data_path) or not os.path.exists(anomalies_path) or not os.path.exists(report_path):
        pytest.fail("Required data or output files are missing, cannot verify correctness.")

    # Read and parse raw data
    with open(raw_data_path, 'rb') as f:
        raw_bytes = f.read()

    num_doubles = len(raw_bytes) // 8
    raw_data = struct.unpack(f'{num_doubles}d', raw_bytes)

    # Compute ground truth mean and standard deviation
    mu = sum(raw_data) / num_doubles
    variance = sum((x - mu) ** 2 for x in raw_data) / num_doubles
    sigma = math.sqrt(variance)

    lower_bound = mu - 3 * sigma
    upper_bound = mu + 3 * sigma

    expected_anomalies = [x for x in raw_data if x < lower_bound or x > upper_bound]

    # Read and parse actual anomalies
    with open(anomalies_path, 'rb') as f:
        actual_bytes = f.read()

    actual_num = len(actual_bytes) // 8
    actual_anomalies = list(struct.unpack(f'{actual_num}d', actual_bytes))

    assert len(expected_anomalies) == len(actual_anomalies), f"Expected {len(expected_anomalies)} anomalies, got {len(actual_anomalies)}."

    expected_sorted = sorted(expected_anomalies)
    actual_sorted = sorted(actual_anomalies)

    for exp, act in zip(expected_sorted, actual_sorted):
        assert math.isclose(exp, act, rel_tol=1e-5), f"Anomaly mismatch: expected {exp}, got {act}."

    # Check report
    report = {}
    with open(report_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                key, val = line.split(':', 1)
                report[key.strip()] = float(val.strip())

    assert 'Mean' in report, "Report missing 'Mean' field."
    assert 'StdDev' in report, "Report missing 'StdDev' field."
    assert 'Anomalies' in report, "Report missing 'Anomalies' field."
    assert 'Time_Seconds' in report, "Report missing 'Time_Seconds' field."

    assert math.isclose(report['Mean'], mu, abs_tol=1e-4), f"Reported mean {report['Mean']} is incorrect, expected ~{mu}."
    assert math.isclose(report['StdDev'], sigma, abs_tol=1e-4), f"Reported StdDev {report['StdDev']} is incorrect, expected ~{sigma}."
    assert int(report['Anomalies']) == len(expected_anomalies), f"Reported anomalies count {int(report['Anomalies'])} is incorrect, expected {len(expected_anomalies)}."
    assert report['Time_Seconds'] > 0, "Benchmark time must be strictly greater than 0."
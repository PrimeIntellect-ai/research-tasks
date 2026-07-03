# test_final_state.py
import os
import json
import hashlib
import csv
import math

def test_analyze_go_exists():
    assert os.path.isfile("/home/user/analyze.go"), "The Go program /home/user/analyze.go does not exist."

def test_report_json_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    assert "file_hash" in data, "Missing 'file_hash' in report.json"
    assert "correlation" in data, "Missing 'correlation' in report.json"
    assert "status" in data, "Missing 'status' in report.json"

def test_report_json_correctness():
    csv_path = "/home/user/data.csv"
    assert os.path.isfile(csv_path), f"The data file {csv_path} is missing."

    with open(csv_path, "rb") as f:
        csv_bytes = f.read()

    expected_hash = hashlib.sha256(csv_bytes).hexdigest()

    # Calculate correlation dynamically
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cpu_vals = []
        latency_vals = []
        for row in reader:
            cpu_vals.append(float(row["cpu"]))
            latency_vals.append(float(row["latency"]))

    n = len(cpu_vals)
    assert n > 0, "CSV file is empty or missing data rows."

    mean_cpu = sum(cpu_vals) / n
    mean_latency = sum(latency_vals) / n

    num = sum((cpu_vals[i] - mean_cpu) * (latency_vals[i] - mean_latency) for i in range(n))
    den_cpu = sum((c - mean_cpu) ** 2 for c in cpu_vals)
    den_latency = sum((l - mean_latency) ** 2 for l in latency_vals)

    if den_cpu == 0 or den_latency == 0:
        expected_correlation = 0.0
    else:
        expected_correlation = num / math.sqrt(den_cpu * den_latency)

    expected_correlation_rounded = round(expected_correlation, 3)
    expected_status = "PASS" if expected_correlation_rounded < 0.700 else "FAIL"

    report_path = "/home/user/report.json"
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["file_hash"] == expected_hash, f"Expected file_hash '{expected_hash}', got '{data['file_hash']}'."
    assert data["correlation"] == expected_correlation_rounded, f"Expected correlation {expected_correlation_rounded}, got {data['correlation']}."
    assert data["status"] == expected_status, f"Expected status '{expected_status}', got '{data['status']}'."
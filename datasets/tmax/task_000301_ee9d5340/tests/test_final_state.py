# test_final_state.py

import os
import json
import pytest

def get_expected_metrics():
    # Read loadavg
    with open("/home/user/mock_proc/loadavg", "r") as f:
        load_parts = f.read().split()
        load1 = float(load_parts[0])
        load5 = float(load_parts[1])
        load15 = float(load_parts[2])

    # Read meminfo
    mem_total = 0
    mem_free = 0
    with open("/home/user/mock_proc/meminfo", "r") as f:
        for line in f:
            if line.startswith("MemTotal:"):
                mem_total = int(line.split()[1])
            elif line.startswith("MemFree:"):
                mem_free = int(line.split()[1])

    return load1, load5, load15, mem_total, mem_free

def calculate_expected_score(load1, load5, load15, mem_total, mem_free):
    load_avg = (load1 + load5 + load15) / 3.0
    mem_ratio = float(mem_free) / float(mem_total)
    return (100.0 - (load_avg * 10.0)) * mem_ratio

def test_shared_library_exists():
    so_path = "/home/user/py_telemetry/libmathops.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} was not created."

def test_python_script_exists():
    py_path = "/home/user/py_telemetry/telemetry.py"
    assert os.path.isfile(py_path), f"Python script {py_path} was not created."

def test_json_output_exists():
    json_path = "/home/user/telemetry_out.json"
    assert os.path.isfile(json_path), f"Output JSON file {json_path} was not created."

def test_json_output_content():
    json_path = "/home/user/telemetry_out.json"
    assert os.path.isfile(json_path), f"Cannot test content, {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "metrics" in data, "Key 'metrics' missing from JSON output."
    assert "score" in data, "Key 'score' missing from JSON output."
    assert "status" in data, "Key 'status' missing from JSON output."

    metrics = data["metrics"]
    expected_keys = ["load1", "load5", "load15", "mem_total_kb", "mem_free_kb"]
    for k in expected_keys:
        assert k in metrics, f"Key '{k}' missing from metrics in JSON output."

    load1, load5, load15, mem_total, mem_free = get_expected_metrics()

    assert pytest.approx(metrics["load1"]) == load1, "load1 metric is incorrect."
    assert pytest.approx(metrics["load5"]) == load5, "load5 metric is incorrect."
    assert pytest.approx(metrics["load15"]) == load15, "load15 metric is incorrect."
    assert metrics["mem_total_kb"] == mem_total, "mem_total_kb metric is incorrect."
    assert metrics["mem_free_kb"] == mem_free, "mem_free_kb metric is incorrect."

    expected_score = calculate_expected_score(load1, load5, load15, mem_total, mem_free)
    expected_score_rounded = round(expected_score, 2)
    expected_status = "CRITICAL" if expected_score_rounded < 50.0 else "OK"

    assert data["score"] == expected_score_rounded, f"Score is incorrect. Expected {expected_score_rounded}, got {data['score']}."
    assert data["status"] == expected_status, f"Status is incorrect. Expected {expected_status}, got {data['status']}."
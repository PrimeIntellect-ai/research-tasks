# test_final_state.py

import os
import pytest

def test_anomalies_output():
    anomalies_file = "/home/user/pipeline/anomalies.txt"
    assert os.path.isfile(anomalies_file), f"Expected file {anomalies_file} does not exist."

    with open(anomalies_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_anomalies = ["REQ003", "REQ005", "REQ006"]

    assert len(lines) == 3, f"Expected exactly 3 anomalies, but found {len(lines)}."
    assert lines == expected_anomalies, f"Anomalies do not match expected output. Got {lines}, expected {expected_anomalies}."

def test_benchmark_output():
    benchmark_file = "/home/user/pipeline/benchmark.txt"
    assert os.path.isfile(benchmark_file), f"Expected file {benchmark_file} does not exist."

    with open(benchmark_file, "r") as f:
        content = f.read().strip()

    assert content, f"File {benchmark_file} is empty."

    try:
        benchmark_val = float(content)
    except ValueError:
        pytest.fail(f"Content of {benchmark_file} is not a valid float: '{content}'")

    assert benchmark_val >= 0, f"Benchmark time should be non-negative, got {benchmark_val}."
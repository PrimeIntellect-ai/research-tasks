# test_final_state.py

import os
import re
import subprocess
import statistics
import pytest

def test_aggregator_fixed():
    file_path = "/home/user/etl/aggregator.cpp"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    with open(file_path, "r") as f:
        content = f.read()
    assert "stoull" in content, "aggregator.cpp does not use std::stoull as requested."
    assert "stod" not in content, "aggregator.cpp still contains std::stod."

def test_aggregator_executable_exists():
    exe_path = "/home/user/etl/aggregator"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_results_csv_correct():
    file_path = "/home/user/etl/results.csv"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    expected = {
        "cat_A": "9007199254740993",
        "cat_B": "9007199254740997",
        "cat_C": "10000000000000005"
    }

    actual = {}
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            assert len(parts) == 2, f"Invalid format in results.csv: {line}"
            actual[parts[0]] = parts[1]

    assert actual == expected, f"results.csv data does not match expected values. Got {actual}"

def test_reproducibility_test_exists_and_passes():
    cpp_path = "/home/user/etl/test_aggregator.cpp"
    exe_path = "/home/user/etl/run_tests"

    assert os.path.isfile(cpp_path), f"Test file {cpp_path} does not exist."
    assert os.path.isfile(exe_path), f"Test executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    result = subprocess.run([exe_path], capture_output=True)
    assert result.returncode == 0, f"run_tests exited with code {result.returncode}, expected 0."

def test_metrics_txt_correct():
    results_path = "/home/user/etl/results.csv"
    metrics_path = "/home/user/etl/metrics.txt"

    assert os.path.isfile(metrics_path), f"File {metrics_path} does not exist."

    # Read actual values from results.csv to compute expected metrics
    values = []
    with open(results_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(",")
                values.append(int(parts[1]))

    expected_mean = statistics.mean(values)
    expected_variance = statistics.variance(values)

    with open(metrics_path, "r") as f:
        content = f.read()

    mean_match = re.search(r"Mean:\s*([0-9.]+)", content)
    assert mean_match is not None, "Mean not found in metrics.txt in the expected format."
    actual_mean = float(mean_match.group(1))

    var_match = re.search(r"Variance:\s*([0-9.eE+]+)", content)
    assert var_match is not None, "Variance not found in metrics.txt in the expected format."
    actual_variance = float(var_match.group(1))

    # Check mean (rounded to 2 decimal places)
    assert abs(actual_mean - expected_mean) < 0.1, f"Expected mean ~{expected_mean:.2f}, got {actual_mean}"

    # Check variance (allow some tolerance due to float formatting/precision)
    rel_error = abs(actual_variance - expected_variance) / expected_variance
    assert rel_error < 0.01, f"Expected variance ~{expected_variance:.2e}, got {actual_variance}"
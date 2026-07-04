# test_final_state.py
import os
import csv
import pytest

def compute_covariance(data):
    n = len(data)
    if n < 2:
        return []

    cols = len(data[0])
    means = [sum(row[i] for row in data) / n for i in range(cols)]

    cov = [[0.0] * cols for _ in range(cols)]
    for i in range(cols):
        for j in range(cols):
            s = sum((row[i] - means[i]) * (row[j] - means[j]) for row in data)
            cov[i][j] = s / (n - 1)

    return cov

def test_covariance_file_exists_and_correct():
    features_path = "/home/user/features.csv"
    cov_path = "/home/user/ml_pipeline/covariance.csv"

    assert os.path.isfile(features_path), f"File {features_path} is missing."
    assert os.path.isfile(cov_path), f"File {cov_path} is missing."

    # Read features
    data = []
    with open(features_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            data.append([float(x) for x in row])

    expected_cov = compute_covariance(data)

    # Read output covariance
    actual_cov = []
    with open(cov_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            actual_cov.append([float(x) for x in row])

    assert len(actual_cov) == len(expected_cov), "Covariance matrix dimensions mismatch."

    for i in range(len(expected_cov)):
        assert len(actual_cov[i]) == len(expected_cov[i]), "Covariance matrix dimensions mismatch."
        for j in range(len(expected_cov[i])):
            assert abs(actual_cov[i][j] - expected_cov[i][j]) < 1e-5, f"Covariance mismatch at ({i}, {j}): expected {expected_cov[i][j]:.6f}, got {actual_cov[i][j]:.6f}"

def test_covariance_file_formatting():
    cov_path = "/home/user/ml_pipeline/covariance.csv"
    assert os.path.isfile(cov_path), f"File {cov_path} is missing."

    with open(cov_path, 'r') as f:
        lines = f.read().strip().split('\n')

    for line in lines:
        parts = line.split(',')
        for part in parts:
            part = part.strip()
            # Check if formatted to exactly 6 decimal places
            assert '.' in part, f"Value {part} is not formatted with a decimal point."
            decimals = part.split('.')[1]
            assert len(decimals) == 6, f"Value {part} is not formatted to exactly 6 decimal places."

def test_benchmark_output_exists_and_correct():
    bench_path = "/home/user/ml_pipeline/benchmark.txt"
    assert os.path.isfile(bench_path), f"File {bench_path} is missing."

    with open(bench_path, 'r') as f:
        content = f.read()

    assert "BenchmarkInference" in content, f"String 'BenchmarkInference' not found in {bench_path}. Benchmark output appears incorrect."

def test_go_files_exist():
    main_go = "/home/user/ml_pipeline/main.go"
    test_go = "/home/user/ml_pipeline/pipeline_test.go"
    go_mod = "/home/user/ml_pipeline/go.mod"

    assert os.path.isfile(main_go), f"File {main_go} is missing."
    assert os.path.isfile(test_go), f"File {test_go} is missing."
    assert os.path.isfile(go_mod), f"File {go_mod} is missing."
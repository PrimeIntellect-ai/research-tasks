# test_final_state.py

import os
import json
import csv
import math
import pytest

def test_go_module_initialized():
    go_mod_path = "/home/user/mlops/go.mod"
    assert os.path.exists(go_mod_path), f"Expected Go module to be initialized at {go_mod_path}"

def test_pipeline_go_exists():
    pipeline_path = "/home/user/mlops/pipeline.go"
    assert os.path.exists(pipeline_path), f"Expected Go program to exist at {pipeline_path}"

def test_benchmark_json():
    benchmark_path = "/home/user/mlops/benchmark.json"
    assert os.path.exists(benchmark_path), f"Benchmark JSON not found at {benchmark_path}"

    with open(benchmark_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("benchmark.json is not valid JSON")

    assert "lines_processed" in data, "lines_processed missing in benchmark.json"
    assert "duration_ns" in data, "duration_ns missing in benchmark.json"

    corpus_path = "/home/user/corpus.txt"
    assert os.path.exists(corpus_path), f"Missing {corpus_path}"
    with open(corpus_path, 'r') as f:
        expected_lines = len(f.readlines())

    assert data["lines_processed"] == expected_lines, f"Expected {expected_lines} lines processed, got {data['lines_processed']}"
    assert isinstance(data["duration_ns"], int), "duration_ns must be an integer"

def test_reduced_csv():
    artifacts_path = "/home/user/mlops/artifacts/reduced.csv"
    assert os.path.exists(artifacts_path), f"Artifacts CSV not found at {artifacts_path}"

    # Compute expected Y
    with open('/home/user/corpus.txt', 'r') as f:
        lines = f.readlines()

    X = []
    for line in lines:
        line = line.lower()
        counts = [0] * 26
        for char in line:
            if 'a' <= char <= 'z':
                counts[ord(char) - ord('a')] += 1
        X.append(counts)

    P = []
    with open('/home/user/projection.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            P.append([float(x) for x in row])

    expected_Y = []
    for i in range(len(X)):
        row_y = []
        for j in range(5):
            val = sum(X[i][k] * P[k][j] for k in range(26))
            row_y.append(val)
        expected_Y.append(row_y)

    # Read actual Y
    actual_Y = []
    with open(artifacts_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                try:
                    actual_Y.append([float(x) for x in row])
                except ValueError:
                    pytest.fail("reduced.csv contains non-float values")

    assert len(actual_Y) == len(expected_Y), f"Expected {len(expected_Y)} rows in reduced.csv, got {len(actual_Y)}"

    for i in range(len(expected_Y)):
        assert len(actual_Y[i]) == 5, f"Expected 5 columns at row {i}, got {len(actual_Y[i])}"
        for j in range(5):
            exp = expected_Y[i][j]
            act = actual_Y[i][j]
            assert math.isclose(exp, act, abs_tol=1e-3), f"Mismatch at row {i} col {j}: expected {exp}, got {act}"
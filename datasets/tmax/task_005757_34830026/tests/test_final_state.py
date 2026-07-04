# test_final_state.py

import os
import json
import pytest

def test_executable_exists():
    exe_path = "/home/user/bin/kmer_counter"
    assert os.path.isfile(exe_path), f"Executable missing: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File is not executable: {exe_path}"

def test_matrix_csv_exists():
    csv_path = "/home/user/data/matrix.csv"
    assert os.path.isfile(csv_path), f"Matrix CSV missing: {csv_path}"
    assert os.path.getsize(csv_path) > 0, f"Matrix CSV is empty: {csv_path}"

def test_go_code_exists():
    go_path = "/home/user/analyze/main.go"
    assert os.path.isfile(go_path), f"Go source file missing: {go_path}"

def test_results_json_exists_and_valid():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Results JSON missing: {results_path}"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Results file is not valid JSON: {results_path}")

    expected_keys = ["condition_number", "A", "b"]
    for key in expected_keys:
        assert key in results, f"Key '{key}' missing in results.json"
        assert isinstance(results[key], (int, float)), f"Key '{key}' must be a number"

def test_results_accuracy():
    truth_path = "/home/user/truth.json"
    results_path = "/home/user/results.json"

    assert os.path.isfile(truth_path), f"Truth JSON missing: {truth_path}"
    assert os.path.isfile(results_path), f"Results JSON missing: {results_path}"

    with open(truth_path, 'r') as f:
        truth = json.load(f)

    with open(results_path, 'r') as f:
        results = json.load(f)

    for key in ["condition_number", "A", "b"]:
        truth_val = truth[key]
        res_val = results[key]
        rel_error = abs((res_val - truth_val) / truth_val)
        assert rel_error < 0.05, (
            f"Value for '{key}' is not within 5% of expected. "
            f"Expected ~{truth_val}, got {res_val} (relative error: {rel_error:.2%})"
        )
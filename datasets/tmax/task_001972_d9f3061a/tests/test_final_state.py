# test_final_state.py

import os
import re
import pytest

def test_similar_experiments_output():
    output_file = "/home/user/similar_experiments.txt"
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_ids = ["EXP-001", "EXP-003", "EXP-005", "EXP-007"]
    actual_ids = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_ids == expected_ids, f"Expected IDs {expected_ids}, but got {actual_ids} in {output_file}."

def test_benchmark_result_output():
    benchmark_file = "/home/user/benchmark_result.txt"
    assert os.path.isfile(benchmark_file), f"Expected benchmark result file {benchmark_file} does not exist."

    with open(benchmark_file, "r") as f:
        content = f.read().strip()

    assert content, f"Benchmark result file {benchmark_file} is empty."

    try:
        val = float(content)
        assert val >= 0, f"Benchmark result must be a positive number, got {val}."
    except ValueError:
        pytest.fail(f"Benchmark result file {benchmark_file} does not contain a valid numeric value, got: '{content}'")

def test_go_mod_exists_and_requires_gonum():
    go_mod_file = "/home/user/mlops/go.mod"
    assert os.path.isfile(go_mod_file), f"Expected go.mod file {go_mod_file} does not exist."

    with open(go_mod_file, "r") as f:
        content = f.read()

    assert "gonum.org/v1/gonum" in content, f"go.mod does not require 'gonum.org/v1/gonum'. Content:\n{content}"

def test_analyze_go_exists():
    go_file = "/home/user/mlops/analyze.go"
    assert os.path.isfile(go_file), f"Expected Go source file {go_file} does not exist."
# test_final_state.py

import os
import json
import re
import pytest

def test_cycles_moved():
    cycles_dir = "/home/user/project_files/cycles"
    assert os.path.isdir(cycles_dir), f"Directory {cycles_dir} does not exist."

    expected_cycles = {"c1.enc", "c2.enc", "c3.enc"}
    actual_cycles = set(os.listdir(cycles_dir))

    for c in expected_cycles:
        assert c in actual_cycles, f"Cyclic file {c} was not moved to {cycles_dir}."

    # Check they are no longer in the main directory
    main_dir = "/home/user/project_files"
    main_files = set(os.listdir(main_dir))
    for c in expected_cycles:
        assert c not in main_files, f"Cyclic file {c} is still in {main_dir}."

def test_results_json():
    results_file = "/home/user/project_files/results.json"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

    with open(results_file, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} does not contain valid JSON.")

    expected_results = {
        "f1.enc": 30.0,
        "f2.enc": 60.0,
        "f3.enc": 30.0,
        "deep1.enc": 1.0,
        "deep2.enc": 2.0,
        "deep3.enc": 3.0,
        "deep4.enc": 4.0,
        "deep5.enc": 5.0
    }

    for fname, expected_val in expected_results.items():
        assert fname in results, f"File {fname} is missing from results.json."
        assert isinstance(results[fname], (int, float)), f"Value for {fname} is not a number."
        assert abs(results[fname] - expected_val) < 1e-6, f"Incorrect value for {fname}. Expected {expected_val}, got {results[fname]}."

    for fname in results:
        assert fname in expected_results, f"Unexpected file {fname} found in results.json."

def test_benchmark_script_exists():
    benchmark_script = "/home/user/benchmark.py"
    assert os.path.isfile(benchmark_script), f"Benchmark script {benchmark_script} does not exist."

def test_benchmark_txt():
    benchmark_txt = "/home/user/benchmark.txt"
    assert os.path.isfile(benchmark_txt), f"Benchmark output {benchmark_txt} does not exist."

    with open(benchmark_txt, "r") as f:
        content = f.read().strip()

    pattern = r"^Deepest File:\s*deep5\.enc,\s*Average Time:\s*[0-9.]+\s*us$"
    assert re.match(pattern, content), f"Benchmark output format is incorrect. Got: '{content}'"
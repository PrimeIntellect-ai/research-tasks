# test_final_state.py

import os
import pytest

def test_c_source_exists():
    path = "/home/user/telemetry_client.c"
    assert os.path.isfile(path), f"Missing C source file at {path}"

def test_compiled_client_exists():
    path = "/home/user/client"
    assert os.path.isfile(path), f"Missing compiled client executable at {path}"
    assert os.access(path, os.X_OK), f"Compiled client at {path} is not executable"

def test_benchmark_script_exists():
    path = "/home/user/benchmark.sh"
    assert os.path.isfile(path), f"Missing benchmark script at {path}"
    assert os.access(path, os.X_OK), f"Benchmark script at {path} is not executable"

def test_benchmark_result():
    path = "/home/user/benchmark_result.txt"
    assert os.path.isfile(path), f"Missing benchmark result file at {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "Total Time: 1500"
    assert content == expected, f"Expected '{expected}' in {path}, but got '{content}'"
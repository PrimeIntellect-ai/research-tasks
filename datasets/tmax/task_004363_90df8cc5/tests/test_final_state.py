# test_final_state.py

import os
import subprocess
import re
import pytest

def test_rust_binary_exists():
    binary_path = "/home/user/workspace/rust_graph/bin/graph_resolver"
    assert os.path.exists(binary_path), f"Rust binary missing at {binary_path}"
    assert os.path.isfile(binary_path), f"Rust path {binary_path} is not a file"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable"

def test_go_tester_exists():
    go_test_file = "/home/user/workspace/go_tester/bench_test.go"
    assert os.path.exists(go_test_file), f"Go test file missing at {go_test_file}"

def test_go_tests_pass():
    go_dir = "/home/user/workspace/go_tester"
    result = subprocess.run(
        ["go", "test"],
        cwd=go_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Go tests failed:\n{result.stdout}\n{result.stderr}"

def test_go_benchmark_throughput():
    go_dir = "/home/user/workspace/go_tester"
    result = subprocess.run(
        ["go", "test", "-bench", ".", "-benchtime=5s"],
        cwd=go_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Go benchmark failed:\n{result.stdout}\n{result.stderr}"

    # Parse ns/op
    match = re.search(r'(\d+(?:\.\d+)?)\s+ns/op', result.stdout)
    assert match is not None, f"Could not parse ns/op from benchmark output:\n{result.stdout}"

    ns_per_op = float(match.group(1))
    throughput = 1e9 / ns_per_op

    assert throughput >= 500.0, f"Throughput {throughput:.2f} ops/sec is below the threshold of 500.0 ops/sec. (ns/op: {ns_per_op})"
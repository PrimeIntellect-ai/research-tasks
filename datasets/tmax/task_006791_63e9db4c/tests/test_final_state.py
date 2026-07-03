# test_final_state.py

import os
import pytest

def test_script_exists():
    script_path = "/home/user/merge_and_resolve.py"
    assert os.path.isfile(script_path), f"Python script not found at {script_path}"

def test_execution_order_content():
    order_path = "/home/user/execution_order.txt"
    assert os.path.isfile(order_path), f"Execution order file not found at {order_path}"

    with open(order_path, "r") as f:
        content = f.read()

    expected_order = "setup_env lint_core build_core build_plugin_a test_plugin_a deploy_all"
    assert content.strip() == expected_order, f"Execution order is incorrect. Got: {content.strip()}"
    assert content.endswith("\n"), "Execution order file must have a trailing newline."

def test_order_diff_content():
    diff_path = "/home/user/order.diff"
    assert os.path.isfile(diff_path), f"Diff file not found at {diff_path}"

    with open(diff_path, "r") as f:
        diff_content = f.read()

    assert "---" in diff_content and "+++" in diff_content, "Diff file does not appear to be a unified diff."
    assert "old_order.txt" in diff_content, "Diff does not contain a reference to old_order.txt."
    assert "execution_order.txt" in diff_content, "Diff does not contain a reference to execution_order.txt."

def test_benchmark_content():
    bench_path = "/home/user/benchmark.txt"
    assert os.path.isfile(bench_path), f"Benchmark output file not found at {bench_path}"

    with open(bench_path, "r") as f:
        bench_content = f.read()

    assert "Maximum resident set size" in bench_content, "Benchmark file does not contain expected output from '/usr/bin/time -v'."
    assert "User time" in bench_content, "Benchmark file does not contain expected output from '/usr/bin/time -v'."
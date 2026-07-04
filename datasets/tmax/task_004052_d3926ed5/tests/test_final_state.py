# test_final_state.py

import os
import sys
import json
import subprocess
import pytest

def test_rust_ecc_installed():
    """Verify that the rust_ecc module has been built and installed into the Python environment."""
    try:
        import rust_ecc
    except ImportError:
        pytest.fail("The 'rust_ecc' module is not installed or cannot be imported. Ensure maturin build and install succeeded.")

def test_worker_uses_rust_ecc():
    """Verify that the worker script has been updated to use the rust_ecc module."""
    worker_path = "/app/worker.py"
    assert os.path.isfile(worker_path), f"{worker_path} is missing."
    with open(worker_path, "r") as f:
        content = f.read()
    assert "rust_ecc" in content, "The worker script does not appear to import or use 'rust_ecc'."

def test_benchmark_performance():
    """Run the benchmark and verify that the throughput meets the threshold."""
    benchmark_path = "/app/benchmark.py"
    result_path = "/tmp/result.json"

    assert os.path.isfile(benchmark_path), f"{benchmark_path} is missing."

    # Execute the benchmark script to generate the JSON output
    cmd = [sys.executable, benchmark_path, "--json-output", result_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Benchmark script failed to execute.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert os.path.isfile(result_path), f"Benchmark script did not create the expected output file at {result_path}."

    # Read the metric
    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON from {result_path}.")

    assert "requests_per_second" in data, f"'requests_per_second' key missing in {result_path}."

    metric = data["requests_per_second"]
    threshold = 800

    assert metric >= threshold, f"Performance threshold not met. Got {metric} requests_per_second, expected >= {threshold}."
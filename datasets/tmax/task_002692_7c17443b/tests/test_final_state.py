# test_final_state.py

import os
import json
import subprocess
import requests
import pytest

def test_libvm_exists():
    """Verify that the Go C-shared library was compiled to the correct location."""
    assert os.path.exists("/app/lib/libvm.so"), "Compiled shared library /app/lib/libvm.so not found."

def test_api_correctness():
    """Verify that the API returns the correct evaluation results."""
    payload = {"batch": ["PUSH 5 PUSH 10 ADD", "PUSH 3 PUSH 4 MUL"]}
    try:
        response = requests.post("http://localhost:8080/api/execute", json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        assert "results" in data, "Response JSON missing 'results' key"
        assert data["results"] == ["15", "12"], f"Expected ['15', '12'], got {data['results']}"
    except Exception as e:
        pytest.fail(f"API correctness test failed: {e}")

def test_benchmark_rps():
    """Verify that the system achieves the required throughput (>= 800 RPS)."""
    # Run the benchmark script to generate the results
    try:
        subprocess.run(["python3", "/app/benchmark.py"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Benchmark script failed to run: {e.stderr}\n{e.stdout}")
    except FileNotFoundError:
        pytest.fail("/app/benchmark.py not found.")

    assert os.path.exists("/app/benchmark_results.json"), "Benchmark results file /app/benchmark_results.json not found."

    with open("/app/benchmark_results.json", "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Failed to parse /app/benchmark_results.json as JSON.")

    assert "rps" in data, "Benchmark results JSON missing 'rps' key."

    try:
        rps = float(data["rps"])
    except ValueError:
        pytest.fail(f"Invalid RPS value in benchmark results: {data['rps']}")

    assert rps >= 800, f"Measured throughput is {rps} RPS, which is below the required threshold of 800 RPS."
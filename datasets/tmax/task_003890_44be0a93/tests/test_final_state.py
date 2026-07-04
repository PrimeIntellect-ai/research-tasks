# test_final_state.py

import subprocess
import re
import pytest

def test_benchmark_throughput():
    """
    Executes the benchmark script and validates that the system throughput
    meets or exceeds the required threshold of 300.0 req/s. This implicitly
    verifies that Nginx, Gunicorn, and QEMU are properly configured, running,
    and communicating.
    """
    cmd = ["python3", "/app/benchmark.py"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        pytest.fail("Benchmark script timed out after 60 seconds.")

    assert result.returncode == 0, (
        f"Benchmark script failed with return code {result.returncode}.\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )

    match = re.search(r"Throughput:\s*([\d\.]+)\s*req/s", result.stdout)
    assert match is not None, (
        f"Could not find throughput metric in benchmark output.\n"
        f"stdout: {result.stdout}"
    )

    throughput = float(match.group(1))
    assert throughput >= 300.0, (
        f"Throughput {throughput} req/s is less than the required threshold of 300.0 req/s."
    )
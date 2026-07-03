# test_final_state.py
import subprocess
import os
import sys

def test_functional_correctness():
    """Verify that the functional tests still pass perfectly."""
    test_path = "/app/authproxy/tests/test_normalize.py"
    assert os.path.isfile(test_path), f"Test file {test_path} is missing."

    # Run pytest on the test file
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Functional tests failed:\n{result.stdout}\n{result.stderr}"

def test_benchmark_performance():
    """Verify that the benchmark runs in <= 0.1 seconds."""
    benchmark_path = "/app/authproxy/benchmark.py"
    assert os.path.isfile(benchmark_path), f"Benchmark file {benchmark_path} is missing."

    # Run the benchmark script
    result = subprocess.run(
        [sys.executable, benchmark_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Benchmark script failed to run:\n{result.stderr}"

    output = result.stdout.strip()
    try:
        runtime = float(output)
    except ValueError:
        assert False, f"Benchmark output is not a valid float: {output}"

    threshold = 0.1
    assert runtime <= threshold, f"Performance regression: benchmark took {runtime:.6f}s, which is > {threshold}s threshold."
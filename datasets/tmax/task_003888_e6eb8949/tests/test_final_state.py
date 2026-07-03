# test_final_state.py
import os
import subprocess
import pytest

def test_libfastcrc_so_exists():
    path = "/app/libfastcrc/libfastcrc.so"
    assert os.path.isfile(path), (
        f"File {path} is missing. "
        "Did you successfully build the library and leave it at the expected path?"
    )

def test_benchmark_speedup():
    benchmark_script = "/app/benchmark.py"
    assert os.path.isfile(benchmark_script), f"Benchmark script {benchmark_script} is missing."

    # Run the benchmark script
    result = subprocess.run(
        ["python3", benchmark_script],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, (
        f"benchmark.py failed to run.\n"
        f"stdout: {result.stdout}\n"
        f"stderr: {result.stderr}"
    )

    metric_file = "/tmp/metric.txt"
    assert os.path.isfile(metric_file), (
        f"Metric file {metric_file} was not created. "
        "The benchmark script might have exited early or failed to load the shared library."
    )

    with open(metric_file, "r") as f:
        content = f.read().strip()

    try:
        speedup = float(content)
    except ValueError:
        pytest.fail(f"Could not parse speedup from {metric_file}. Content: {content}")

    assert speedup >= 15.0, (
        f"Speedup is {speedup:.2f}x, which is less than the required threshold of 15.0x. "
        "Further optimization of the C implementation is required."
    )
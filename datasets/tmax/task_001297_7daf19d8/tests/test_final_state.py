# test_final_state.py

import os
import subprocess
import pytest

APP_DIR = "/home/user/app"
INGEST_BIN = os.path.join(APP_DIR, "ingest")
BENCHMARK_SCRIPT = os.path.join(APP_DIR, "benchmark.py")

def test_ingest_binary_exists():
    """Ensure that the ingest binary has been successfully compiled."""
    assert os.path.isfile(INGEST_BIN), (
        f"Compiled binary not found at {INGEST_BIN}. "
        "Make sure you fixed the compiler/linker errors and successfully built the project."
    )
    assert os.access(INGEST_BIN, os.X_OK), f"File at {INGEST_BIN} is not executable."

def test_throughput_metric():
    """
    Run the benchmark script to measure the throughput of valid JSON records
    correctly inserted into the Redis list.
    """
    assert os.path.isfile(BENCHMARK_SCRIPT), f"Benchmark script missing at {BENCHMARK_SCRIPT}"

    try:
        # The benchmark script simulates the stream, runs ./ingest, checks Redis, 
        # and outputs the records/sec.
        result = subprocess.run(
            ["python3", BENCHMARK_SCRIPT],
            cwd=APP_DIR,
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(
            f"Benchmark script failed with exit code {e.returncode}.\n"
            f"Stdout:\n{e.stdout}\n"
            f"Stderr:\n{e.stderr}\n"
            "This usually means the ingestion service crashed, failed to connect, "
            "or failed to parse packets correctly."
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Benchmark script timed out after 30 seconds.")

    output = result.stdout.strip()

    # The benchmark script is expected to return a numerical value representing records/sec.
    # We take the last line in case there are other print statements.
    try:
        lines = output.split('\n')
        throughput = float(lines[-1].strip())
    except ValueError:
        pytest.fail(
            f"Could not parse the benchmark script output as a float.\n"
            f"Output was:\n{output}"
        )

    target_throughput = 2000.0
    assert throughput >= target_throughput, (
        f"Throughput is too low. Measured: {throughput:.2f} records/sec. "
        f"Target: >= {target_throughput} records/sec.\n"
        "Make sure you have optimized the performance bottleneck (e.g., moving "
        "redisConnect and redisFree outside of the packet processing loop)."
    )
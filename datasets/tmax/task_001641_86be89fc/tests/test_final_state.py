# test_final_state.py
import os
import subprocess
import time
import pytest

def test_status_file():
    path = "/home/user/status.txt"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert "READY" in content, f"Expected 'READY' in {path}, but found: '{content}'"

def test_executable_exists():
    path = "/app/libmathgraph-1.4.2/mathgraph_cli"
    assert os.path.isfile(path), f"Executable {path} is missing. Did the build succeed?"
    assert os.access(path, os.X_OK), f"File {path} exists but is not executable."

def test_execution_time_and_correctness():
    exe_path = "/app/libmathgraph-1.4.2/mathgraph_cli"
    data_path = "/app/test_data/large_graph.mtx"

    assert os.path.isfile(data_path), f"Test data {data_path} is missing."

    # Measure execution time
    start_time = time.perf_counter()
    result = subprocess.run(
        [exe_path, ">=1.4.0", data_path],
        capture_output=True,
        text=True
    )
    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    # Ensure the program completed successfully
    assert result.returncode == 0, (
        f"Execution of {exe_path} failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )

    # Assert performance threshold
    threshold = 0.5
    assert elapsed_time <= threshold, (
        f"Execution time metric failed: took {elapsed_time:.3f} seconds, "
        f"which exceeds the threshold of {threshold} seconds. "
        "Ensure -O3 optimization is used and the memory safety bug is fixed."
    )
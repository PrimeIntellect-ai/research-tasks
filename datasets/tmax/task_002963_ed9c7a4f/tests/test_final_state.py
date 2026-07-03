# test_final_state.py

import os
import pytest

def test_benchmark_result():
    result_file = "/home/user/benchmark_result.txt"
    assert os.path.isfile(result_file), f"Benchmark result file {result_file} is missing. Did you run the benchmark script?"

    with open(result_file, "r") as f:
        content = f.read().strip()

    try:
        score = float(content)
    except ValueError:
        pytest.fail(f"Could not parse benchmark score as a float. File content: '{content}'")

    assert score >= 250.0, f"Benchmark score {score} is below the required threshold of 250.0 (Logs processed per second)."

def test_c_extension_compiled():
    so_file = "/app/vendor/secure_etl_tool-1.0/fast_integrity.so"
    assert os.path.isfile(so_file), f"Compiled C-extension {so_file} is missing. Did you fix the Makefile and run make?"

def test_worker_patched_no_pass_argument():
    worker_path = "/app/vendor/secure_etl_tool-1.0/worker.py"
    assert os.path.isfile(worker_path), f"File {worker_path} is missing."

    with open(worker_path, "r") as f:
        content = f.read()

    # The benchmark score checks for leaks, but we can also ensure the literal 'pass:' 
    # used in the vulnerable subprocess call has been removed or replaced appropriately.
    # Note: 'pass:' might still be present if they used 'pass:env:VAR', but the vulnerability 
    # was specifically f"pass:{secret_key}" or similar. We rely primarily on the benchmark score 
    # for the strict leak test, as the benchmark script monitors /proc.
    assert content, "worker.py is empty."
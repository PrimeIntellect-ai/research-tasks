# test_final_state.py

import os
import time
import subprocess
import pytest

def test_deadlock_detector_performance_and_correctness():
    c_source = "/home/user/deadlock_detector.c"
    assert os.path.isfile(c_source), f"Missing source file: {c_source}"

    # Compile the C program
    compiled_bin = "/tmp/deadlock_detector_test"
    compile_res = subprocess.run(
        ["gcc", "-O3", c_source, "-o", compiled_bin],
        capture_output=True, text=True
    )
    assert compile_res.returncode == 0, f"Compilation failed:\n{compile_res.stderr}"

    hidden_log = "/app/hidden_massive_log.csv"
    assert os.path.isfile(hidden_log), f"Hidden log missing: {hidden_log}"

    # Run the compiled program and measure execution time
    start_time = time.time()
    run_res = subprocess.run(
        [compiled_bin, hidden_log, "13.73"],
        capture_output=True, text=True
    )
    duration = time.time() - start_time

    assert run_res.returncode == 0, f"Program crashed or returned non-zero:\n{run_res.stderr}"

    # Verify the output correctness
    output = run_res.stdout.strip()
    expected_output = "8392,10293,44021,99201"
    assert output == expected_output, f"Incorrect deadlock cycle detected. Expected '{expected_output}', got '{output}'"

    # Verify the performance metric
    assert duration <= 1.5, f"Execution too slow: {duration:.3f}s (threshold 1.5s)"

def test_public_result_exists():
    result_file = "/home/user/deadlock_result.txt"
    assert os.path.isfile(result_file), f"Missing result file: {result_file}"
    with open(result_file, "r") as f:
        content = f.read().strip()
    assert len(content) > 0, f"Result file {result_file} is empty"
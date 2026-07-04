# test_final_state.py

import os
import subprocess
import time
import pytest

def test_fast_detector_correctness_and_speedup():
    naive_src = "/app/naive.cpp"
    naive_bin = "/tmp/naive"
    fast_bin = "/home/user/fast_detector"
    output_file = "/home/user/deadlocks.txt"
    naive_output = "/tmp/naive_deadlocks.txt"

    # Ensure the fast detector was compiled
    assert os.path.exists(fast_bin), f"Executable {fast_bin} not found. Did you compile your program?"
    assert os.access(fast_bin, os.X_OK), f"File {fast_bin} is not executable."

    # Compile the naive implementation
    compile_cmd = ["g++", "-O3", naive_src, "-o", naive_bin]
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile naive implementation: {e.stderr}")

    # Clean up any existing output file before running naive
    if os.path.exists(output_file):
        os.remove(output_file)

    # Run naive implementation and measure time
    t0 = time.perf_counter()
    try:
        subprocess.run([naive_bin], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Naive implementation failed to run: {e.stderr}")
    t1 = time.perf_counter()
    naive_time = t1 - t0

    # Ensure naive produced the output, then move it
    assert os.path.exists(output_file), f"Naive implementation did not produce {output_file}."
    os.rename(output_file, naive_output)

    # Run user's fast implementation and measure time
    t0 = time.perf_counter()
    try:
        subprocess.run([fast_bin], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Your fast_detector failed to run: {e.stderr}")
    t1 = time.perf_counter()
    fast_time = t1 - t0

    # Ensure user produced the output
    assert os.path.exists(output_file), f"Your program did not produce {output_file}."

    # Compare outputs for correctness
    with open(naive_output, 'r') as f:
        naive_lines = f.read().splitlines()
    with open(output_file, 'r') as f:
        fast_lines = f.read().splitlines()

    assert len(fast_lines) > 0, "Your output file is empty."
    assert naive_lines == fast_lines, "The output of fast_detector does not exactly match the reference output. Check your filtering rules and cycle detection."

    # Calculate and assert speedup
    speedup = naive_time / fast_time
    assert speedup >= 20.0, f"Speedup is {speedup:.2f}x (Naive: {naive_time:.4f}s, Yours: {fast_time:.4f}s), which is less than the required 20.0x threshold."
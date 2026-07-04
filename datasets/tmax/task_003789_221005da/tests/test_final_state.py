# test_final_state.py

import os
import subprocess
import time
import pytest

def test_optimized_w1_performance_and_accuracy():
    cpp_file = "/home/user/optimized_w1.cpp"
    exe_file = "/home/user/optimized_w1"

    assert os.path.isfile(cpp_file), f"The optimized C++ file {cpp_file} is missing."

    # Compile the agent's code
    compile_cmd = ["g++", "-O3", cpp_file, "-o", exe_file]
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Compilation failed:\n{e.stderr}")

    assert os.path.isfile(exe_file), "Executable was not created after compilation."

    # Run the compiled program and measure execution time
    start_time = time.time()
    try:
        res = subprocess.run(
            [exe_file, "50000", "0.5", "0.15"], 
            capture_output=True, 
            text=True, 
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution failed:\n{e.stderr}")
    end_time = time.time()

    agent_time = end_time - start_time

    # Parse the output
    output_str = res.stdout.strip()
    try:
        agent_val = float(output_str)
    except ValueError:
        pytest.fail(f"Could not parse output as float. Output was: {output_str}")

    # Calculate speedup based on the ~100s baseline for naive O(M*N)
    speedup = 100.0 / agent_time

    # Assertions
    assert speedup >= 50.0, f"Speedup {speedup:.2f}x is below the 50.0x threshold (Agent time: {agent_time:.4f}s)."

    # Check if the computed Wasserstein distance is reasonable. 
    # For U(0,1) vs N(0.5, 0.15), the W1 distance is approximately ~0.07.
    # We check that it's strictly positive and within a reasonable bound.
    assert agent_val > 0.0, f"Wasserstein distance must be > 0.0, got {agent_val}"
    assert agent_val < 0.2, f"Wasserstein distance {agent_val} is too large to be correct for U(0,1) vs N(0.5, 0.15)."
# test_final_state.py

import os
import subprocess
import time
import pytest

def max_subarray_sum(arr):
    if not arr:
        return 0
    max_so_far = float('-inf')
    curr_max = 0
    for x in arr:
        curr_max = max(x, curr_max + x)
        max_so_far = max(max_so_far, curr_max)
    return max_so_far

def test_optimized_cpp_exists():
    assert os.path.exists("/home/user/optimized.cpp"), "/home/user/optimized.cpp does not exist."
    assert os.path.isfile("/home/user/optimized.cpp"), "/home/user/optimized.cpp is not a file."

def test_run_tests_sh_exists_and_executable():
    script_path = "/home/user/run_tests.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_result_log_and_correctness():
    log_path = "/home/user/result.log"
    large_txt_path = "/home/user/large.txt"

    assert os.path.exists(large_txt_path), f"{large_txt_path} does not exist. Did run_tests.sh create it?"
    assert os.path.exists(log_path), f"{log_path} does not exist. Did run_tests.sh run successfully?"

    with open(large_txt_path, "r") as f:
        content = f.read().split()

    arr = []
    for x in content:
        try:
            arr.append(int(x))
        except ValueError:
            pass

    expected_sum = max_subarray_sum(arr)
    expected_output = f"Max subarray sum: {expected_sum}"

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    assert expected_output in log_content, f"Expected '{expected_output}' in {log_path}, but got '{log_content}'"

def test_optimized_performance():
    cpp_path = "/home/user/optimized.cpp"
    bin_path = "/tmp/test_optimized_bin"
    large_txt_path = "/home/user/large.txt"

    assert os.path.exists(cpp_path), "optimized.cpp is missing."
    assert os.path.exists(large_txt_path), "large.txt is missing."

    # Compile the optimized code
    compile_proc = subprocess.run(["g++", "-O3", cpp_path, "-o", bin_path], capture_output=True)
    assert compile_proc.returncode == 0, f"Failed to compile optimized.cpp:\n{compile_proc.stderr.decode()}"

    # Run and time it
    start_time = time.time()
    run_proc = subprocess.run([bin_path, large_txt_path], capture_output=True, text=True)
    end_time = time.time()

    assert run_proc.returncode == 0, "optimized_bin failed to execute."

    elapsed = end_time - start_time
    assert elapsed < 1.0, f"Optimized binary took too long: {elapsed:.2f} seconds. Expected < 1.0s."
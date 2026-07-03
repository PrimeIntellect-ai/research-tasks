# test_final_state.py

import os
import subprocess
import time
import pytest

def test_dataset_extracted():
    dataset_path = "/home/user/dataset.txt"
    assert os.path.isfile(dataset_path), f"File {dataset_path} does not exist."

    with open(dataset_path, "r") as f:
        content = f.read()

    expected_text = "pkgA>=1.0.0,<2.0.0\npkgB>=1.5.0\npkgA<=1.9.0\npkgC>=0.0.1\n"
    assert content == expected_text, f"Extracted dataset content does not match expected. Got:\n{content}"

def test_cpp_compilation_and_performance():
    cpp_path = "/home/user/resolver.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} does not exist."

    binary_path = "/home/user/resolver"

    # Compile the C++ program
    compile_cmd = ["g++", "-O3", "-pthread", "-std=c++20", cpp_path, "-o", binary_path]
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Compilation failed:\n{compile_proc.stderr}"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} was not created."

    # Execute and measure time
    start_time = time.perf_counter()
    run_proc = subprocess.run([binary_path], capture_output=True, text=True)
    end_time = time.perf_counter()

    assert run_proc.returncode == 0, f"Execution failed:\n{run_proc.stderr}"

    execution_time = end_time - start_time
    threshold = 0.5

    # Check output
    expected_output = "pkgA: 1.9.0\npkgB: 1.5.0\npkgC: 0.0.1"
    output = run_proc.stdout.strip()
    assert output == expected_output, f"Output did not match expected. Got:\n{output}\nExpected:\n{expected_output}"

    # Check performance metric
    assert execution_time <= threshold, f"Execution time {execution_time:.4f}s exceeded threshold of {threshold}s."
# test_final_state.py

import os
import subprocess
import time
import filecmp
import pytest

def test_graph_etl_exists_and_executable():
    path = "/home/user/graph_etl"
    assert os.path.isfile(path), f"Missing compiled C program: {path}"
    assert os.access(path, os.X_OK), f"Program is not executable: {path}"

def test_graph_etl_correctness_and_speedup():
    c_bin = "/home/user/graph_etl"
    py_script = "/home/user/slow_reference.py"
    input_csv = "/home/user/graph_results.csv"

    out_c = "/home/user/output_c.csv"
    out_py = "/home/user/output_py.csv"

    args = [
        "--input", input_csv,
        "--filter-label", "Person",
        "--sort-prop", "score",
        "--limit", "100",
        "--offset", "10"
    ]

    # Run Python reference
    start_py = time.time()
    subprocess.run(["python3", py_script] + args + ["--output", out_py], check=True)
    time_py = time.time() - start_py

    # Run C program
    start_c = time.time()
    subprocess.run([c_bin] + args + ["--output", out_c], check=True)
    time_c = time.time() - start_c

    # Check outputs
    assert os.path.exists(out_c), "C program did not produce the output file."
    assert os.path.exists(out_py), "Python program did not produce the output file."

    # Read outputs to compare
    with open(out_c, 'r') as f_c, open(out_py, 'r') as f_py:
        c_lines = f_c.read().strip().splitlines()
        py_lines = f_py.read().strip().splitlines()

    assert c_lines == py_lines, "Output of C program does not match Python reference."

    # Check speedup
    speedup = time_py / time_c if time_c > 0 else float('inf')
    assert speedup >= 5.0, f"Speedup is {speedup:.2f}, which is less than the threshold of 5.0 (C time: {time_c:.4f}s, Py time: {time_py:.4f}s)"
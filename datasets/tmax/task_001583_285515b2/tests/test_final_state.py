# test_final_state.py

import os
import subprocess
import time
import pytest

def run_cmd(cmd):
    start = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    end = time.time()
    return res, end - start

def test_fast_path_speedup():
    c_file = "/home/user/fast_path.c"
    binary_file = "/home/user/fast_path"

    assert os.path.isfile(c_file), f"Source file missing: {c_file}"

    # Compile the C file to ensure we are testing the latest version with optimizations
    compile_cmd = ["gcc", "-O3", c_file, "-o", binary_file, "-lm"]
    compile_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_res.returncode == 0, f"Compilation failed:\n{compile_res.stderr}"

    assert os.path.isfile(binary_file), f"Binary missing: {binary_file}"
    assert os.access(binary_file, os.X_OK), f"Binary is not executable: {binary_file}"

    edges_test = "/test/edges_test.csv"
    queries_test = "/test/queries_test.txt"
    oracle_bin = "/app/graph_oracle"

    assert os.path.isfile(edges_test), f"Test edges missing: {edges_test}"
    assert os.path.isfile(queries_test), f"Test queries missing: {queries_test}"
    assert os.path.isfile(oracle_bin), f"Oracle binary missing: {oracle_bin}"

    # Run oracle
    oracle_res, oracle_time = run_cmd([oracle_bin, edges_test, queries_test])
    assert oracle_res.returncode == 0, f"Oracle failed:\n{oracle_res.stderr}"
    oracle_out = oracle_res.stdout.strip()

    # Run agent
    agent_res, agent_time = run_cmd([binary_file, edges_test, queries_test])
    assert agent_res.returncode == 0, f"Agent binary failed:\n{agent_res.stderr}"
    agent_out = agent_res.stdout.strip()

    # Check correctness
    assert agent_out == oracle_out, "Agent output does not match the oracle output exactly."

    # Check speedup
    speedup = oracle_time / agent_time
    assert speedup >= 50.0, f"Speedup is {speedup:.2f}x, which is less than the required 50.0x threshold."
# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_executable_exists_and_runs():
    exe_path = "/home/user/rate_limiter/rate_limit_checker"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing. Did you run make?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    # Test running it
    log_path = "/home/user/rate_limiter/requests.log"
    result = subprocess.run([exe_path, log_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {exe_path} failed with return code {result.returncode}."

    expected_output = (
        "ALLOW 192.168.1.1 10\n"
        "ALLOW 192.168.1.1 12\n"
        "DENY 192.168.1.1 13\n"
        "ALLOW 10.0.0.1 14\n"
        "ALLOW 192.168.1.1 20\n"
        "ALLOW 10.0.0.1 15\n"
        "DENY 10.0.0.1 16\n"
    )
    assert result.stdout == expected_output, f"Output of {exe_path} does not match expected rate limiting logic."

def test_results_txt():
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

    with open(results_path, "r") as f:
        content = f.read()

    expected_output = (
        "ALLOW 192.168.1.1 10\n"
        "ALLOW 192.168.1.1 12\n"
        "DENY 192.168.1.1 13\n"
        "ALLOW 10.0.0.1 14\n"
        "ALLOW 192.168.1.1 20\n"
        "ALLOW 10.0.0.1 15\n"
        "DENY 10.0.0.1 16\n"
    )
    assert content == expected_output, f"Content of {results_path} does not match the expected output."

def test_bench_sh():
    bench_path = "/home/user/bench.sh"
    assert os.path.isfile(bench_path), f"Benchmark script {bench_path} is missing."

    st = os.stat(bench_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Benchmark script {bench_path} is not executable."

    with open(bench_path, "r") as f:
        content = f.read()

    # Check for 500 iterations in some form
    assert "500" in content, f"Benchmark script {bench_path} does not seem to contain the number 500 for the loop."

    # Check for the command
    assert "rate_limit_checker" in content, f"Benchmark script {bench_path} does not call rate_limit_checker."
    assert "requests.log" in content, f"Benchmark script {bench_path} does not pass requests.log as argument."
    assert "> /dev/null" in content or ">/dev/null" in content, f"Benchmark script {bench_path} does not redirect output to /dev/null."
# test_final_state.py

import os
import subprocess
import pytest

def test_debug_report_contents():
    report_path = "/home/user/debug_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    commit_file = "/tmp/.buggy_commit"
    assert os.path.isfile(commit_file), f"Truth file {commit_file} is missing."

    with open(commit_file, "r") as f:
        expected_commit = f.read().strip()

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "Report file must contain at least two lines."
    assert expected_commit in lines[0], f"First line does not contain the correct buggy commit hash. Found: {lines[0]}"
    assert "MALFORMED_X99_ABORT" in lines[1], f"Second line does not contain the correct trigger payload. Found: {lines[1]}"

def test_memory_leak_fixed():
    cpp_file = "/home/user/service_repo/src/server.cpp"
    assert os.path.isfile(cpp_file), f"Source file {cpp_file} is missing."

    test_binary = "/tmp/test_service"
    compile_cmd = ["g++", "-std=c++14", cpp_file, "-o", test_binary]
    try:
        subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile {cpp_file}:\n{e.stderr.decode()}")

    env = os.environ.copy()
    env["CONFIG_ENV"] = "production"

    valgrind_cmd = [
        "valgrind", 
        "--leak-check=full", 
        test_binary, 
        "MALFORMED_X99_ABORT"
    ]

    try:
        result = subprocess.run(valgrind_cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        pytest.fail("valgrind is not installed or not in PATH.")

    stderr_output = result.stderr.decode()

    # Valgrind outputs to stderr. We check for indicators that memory was properly freed.
    leak_fixed = "definitely lost: 0 bytes" in stderr_output or "All heap blocks were freed" in stderr_output
    assert leak_fixed, f"Memory leak is still present or valgrind failed. Valgrind output:\n{stderr_output}"
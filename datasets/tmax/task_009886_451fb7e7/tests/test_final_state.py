# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE = "/home/user/pr_review"

def test_makefile_builds_correctly():
    # Make sure we can clean and build using the provided Makefile
    clean_result = subprocess.run(["make", "clean"], cwd=WORKSPACE, capture_output=True)
    assert clean_result.returncode == 0, f"'make clean' failed: {clean_result.stderr.decode()}"

    build_result = subprocess.run(["make"], cwd=WORKSPACE, capture_output=True)
    assert build_result.returncode == 0, f"'make' failed to build log_parser. Error:\n{build_result.stderr.decode()}"

    executable_path = os.path.join(WORKSPACE, "log_parser")
    assert os.path.isfile(executable_path), "log_parser executable was not created by 'make'."
    assert os.access(executable_path, os.X_OK), "log_parser is not executable."

def test_output_files_exist():
    py_out = os.path.join(WORKSPACE, "py_out.txt")
    cpp_out = os.path.join(WORKSPACE, "cpp_out.txt")
    valgrind_out = os.path.join(WORKSPACE, "valgrind_report.txt")

    assert os.path.isfile(py_out), f"{py_out} is missing. Did you run the Python script?"
    assert os.path.isfile(cpp_out), f"{cpp_out} is missing. Did you run the C++ program?"
    assert os.path.isfile(valgrind_out), f"{valgrind_out} is missing. Did you run Valgrind?"

def test_execution_correctness():
    py_out = os.path.join(WORKSPACE, "py_out.txt")
    cpp_out = os.path.join(WORKSPACE, "cpp_out.txt")

    with open(py_out, "r") as f:
        py_content = f.read().strip()

    with open(cpp_out, "r") as f:
        cpp_content = f.read().strip()

    assert py_content == cpp_content, "The output of the C++ program does not exactly match the Python program."

    # Verify the actual expected content based on dummy_logs.txt
    expected_lines = [
        "ERR05: 1",
        "ERR12: 2",
        "ERR99: 1"
    ]
    for line in expected_lines:
        assert line in cpp_content, f"Expected output line '{line}' missing from cpp_out.txt."

def test_valgrind_memory_leak_resolved():
    valgrind_out = os.path.join(WORKSPACE, "valgrind_report.txt")

    with open(valgrind_out, "r") as f:
        valgrind_content = f.read()

    # Check for 0 bytes definitely lost
    assert "definitely lost: 0 bytes in 0 blocks" in valgrind_content, (
        "Valgrind report does not indicate 'definitely lost: 0 bytes in 0 blocks'. "
        "The memory leak may not be fully resolved."
    )
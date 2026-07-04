# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace/librest_parser"

def test_make_succeeds():
    """Verify that the project builds successfully."""
    # Run make clean and make
    subprocess.run(["make", "clean"], cwd=WORKSPACE_DIR, capture_output=True)
    result = subprocess.run(["make"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with output:\n{result.stderr}\n{result.stdout}"

    so_path = os.path.join(WORKSPACE_DIR, "librest_parser.so")
    assert os.path.isfile(so_path), f"Expected shared library {so_path} to be built."

def test_linking_issue_fixed():
    """Verify that the global variable linking issue is resolved."""
    header_path = os.path.join(WORKSPACE_DIR, "include", "string_buf.h")
    assert os.path.isfile(header_path), f"Header file missing: {header_path}"

    with open(header_path, "r") as f:
        content = f.read()

    # The bug was "int global_alloc_count = 0;"
    # It should be changed to "extern int global_alloc_count;" or removed.
    # We just check that the exact problematic definition is gone or modified.
    # A simple check is that if it's there, it must have 'extern'
    lines = content.split('\n')
    for line in lines:
        if "global_alloc_count" in line and not line.strip().startswith("//"):
            if "int global_alloc_count" in line:
                assert "extern" in line, "global_alloc_count must be declared as extern in the header to fix the linking error."

def test_memory_leak_fixed():
    """Verify that the memory leak in string_buf_free is fixed."""
    source_path = os.path.join(WORKSPACE_DIR, "src", "string_buf.c")
    assert os.path.isfile(source_path), f"Source file missing: {source_path}"

    with open(source_path, "r") as f:
        content = f.read()

    # We check if free(buf) is now present
    assert "free(buf)" in content.replace("free(buf->data)", ""), "The memory leak is not fixed. Missing free(buf) in string_buf.c."

def test_run_tests_executable_exists():
    """Verify that the run_tests executable was built."""
    run_tests_path = os.path.join(WORKSPACE_DIR, "run_tests")
    assert os.path.isfile(run_tests_path), f"Executable missing: {run_tests_path}"
    assert os.access(run_tests_path, os.X_OK), f"File is not executable: {run_tests_path}"

def test_test_results_log():
    """Verify the contents of test_results.log."""
    log_path = os.path.join(WORKSPACE_DIR, "test_results.log")
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_output = "TEST 1: PASS\nTEST 2: PASS\nTEST 3: PASS"
    assert expected_output in content, f"Log file does not contain the expected output. Found:\n{content}"

def test_valgrind_clean():
    """Verify that Valgrind reports 0 leaks and 0 errors for run_tests."""
    run_tests_path = os.path.join(WORKSPACE_DIR, "run_tests")
    assert os.path.isfile(run_tests_path), "run_tests executable not found for valgrind check."

    result = subprocess.run(
        ["valgrind", "--leak-check=full", "--error-exitcode=1", "./run_tests"],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True
    )

    # Check for 0 definitely lost
    assert "definitely lost: 0 bytes" in result.stderr, f"Valgrind reported memory leaks:\n{result.stderr}"
    assert result.returncode == 0, f"Valgrind reported errors:\n{result.stderr}"
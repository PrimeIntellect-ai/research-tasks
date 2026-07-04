# test_final_state.py

import os
import re
import pytest

WORKSPACE_DIR = "/home/user/polyglot_auth"

def test_test_results_log():
    """Test that the end-to-end test results log exists and indicates success."""
    log_path = os.path.join(WORKSPACE_DIR, "test_results.log")
    assert os.path.isfile(log_path), f"Test results log {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "E2E_TESTS_PASSED", f"Expected 'E2E_TESTS_PASSED' in test_results.log, but found: '{content}'"

def test_cmake_fixed():
    """Test that CMakeLists.txt was updated to build a SHARED library."""
    cmake_path = os.path.join(WORKSPACE_DIR, "CMakeLists.txt")
    assert os.path.isfile(cmake_path), f"{cmake_path} does not exist."

    with open(cmake_path, "r") as f:
        content = f.read()

    assert "SHARED" in content, "CMakeLists.txt does not contain 'SHARED'. The library must be built dynamically."
    assert "STATIC" not in content, "CMakeLists.txt still contains 'STATIC', which means it is not building a shared library."

def test_c_source_fixed():
    """Test that the C source file's memory allocation bug was fixed."""
    c_path = os.path.join(WORKSPACE_DIR, "lib", "secure_hash.c")
    assert os.path.isfile(c_path), f"{c_path} does not exist."

    with open(c_path, "r") as f:
        content = f.read()

    # Ensure the exact buggy malloc(len) is gone
    buggy_malloc = re.search(r'malloc\s*\(\s*len\s*\)', content)
    assert not buggy_malloc, "secure_hash.c still contains the buggy 'malloc(len)' without accounting for the null terminator."

    # Ensure there is a safe allocation like malloc(len + 1)
    safe_alloc = re.search(r'(malloc|calloc)\s*\([^;]*len\s*\+\s*[1-9][0-9]*[^;]*\)', content)
    assert safe_alloc is not None, "secure_hash.c does not appear to safely allocate 'len + 1' (or more) bytes for the string."
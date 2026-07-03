# test_final_state.py

import os
import pytest

def test_libprocessor_compiled():
    """Check if the shared library was compiled in the correct location."""
    so_path = "/home/user/src/libprocessor.so"
    assert os.path.isfile(so_path), f"The compiled shared library {so_path} is missing."

def test_server_py_updated():
    """Check if server.py was updated to load the correct library."""
    server_path = "/home/user/src/server.py"
    assert os.path.isfile(server_path), f"The file {server_path} is missing."
    with open(server_path, "r") as f:
        content = f.read()
    assert "/usr/lib/libprocessor.so" not in content, "server.py still contains the hardcoded broken library path."
    assert "libprocessor.so" in content, "server.py does not seem to load the new libprocessor.so."

def test_processor_c_fixed():
    """Check if processor.c was modified to include bounds checking."""
    c_path = "/home/user/src/processor.c"
    assert os.path.isfile(c_path), f"The file {c_path} is missing."
    with open(c_path, "r") as f:
        content = f.read()

    # We don't check for exact syntax, but we expect MAX_TOKENS or a literal 5 to be used in a condition
    # related to token_count.
    assert "MAX_TOKENS" in content or "5" in content, "processor.c does not seem to enforce MAX_TOKENS."

def test_diff_result_correct():
    """Check if the final diff_result.txt contains the correct symmetric difference."""
    result_path = "/home/user/diff_result.txt"
    assert os.path.isfile(result_path), f"The output file {result_path} is missing. Did the client run successfully?"

    with open(result_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Expected logic:
    # A = "alpha beta gamma delta epsilon zeta eta theta"
    # B = "alpha beta gamma omega epsilon zeta eta iota"
    # Max tokens = 5
    # A_truncated = ["alpha", "beta", "gamma", "delta", "epsilon"]
    # B_truncated = ["alpha", "beta", "gamma", "omega", "epsilon"]
    # Symmetric diff = ["delta", "omega"]
    # Sorted = ["delta", "omega"]

    expected = ["delta", "omega"]
    assert lines == expected, f"Expected symmetric difference {expected}, but got {lines}."
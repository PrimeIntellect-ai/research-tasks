# test_final_state.py

import os
import pytest

def compute_expected_sequence(n: int) -> int:
    seq = [1, 1]
    for i in range(2, n + 1):
        seq.append(seq[i-1] + 2 * seq[i-2])
    return seq[n]

def test_rust_engine_compiled():
    # The rust engine should be compiled into a shared library
    so_path = "/home/user/math_integration/rust_engine/target/debug/librust_engine.so"
    assert os.path.exists(so_path), f"Compiled Rust library not found at {so_path}. Did you run 'cargo build'?"

def test_server_py_fixed():
    # Check that the naive string comparison bug is fixed
    server_py = "/home/user/math_integration/server.py"
    assert os.path.exists(server_py), f"Missing server.py at {server_py}"
    with open(server_py, "r") as f:
        content = f.read()
        assert '< "2.1.0"' not in content, "server.py still contains the naive string comparison bug for the version."

def test_result_file_correct():
    # Check that the client ran and produced the correct output
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"Result file not found at {result_path}. Did the client script run successfully?"

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected_result = str(compute_expected_sequence(20))
    assert content == expected_result, f"Result file contains '{content}', but expected '{expected_result}'."
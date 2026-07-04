# test_final_state.py

import os
import ctypes
import pytest

APP_DIR = "/home/user/app"
C_FILE = os.path.join(APP_DIR, "libverifier.c")
SO_FILE = os.path.join(APP_DIR, "libverifier.so")
PY_FILE = os.path.join(APP_DIR, "benchmark.py")
LOG_FILE = os.path.join(APP_DIR, "benchmark_results.log")

def test_files_exist():
    """Verify that all required files have been created."""
    assert os.path.exists(APP_DIR), f"Directory {APP_DIR} does not exist."
    assert os.path.isfile(C_FILE), f"C source file {C_FILE} does not exist."
    assert os.path.isfile(SO_FILE), f"Shared library {SO_FILE} does not exist."
    assert os.path.isfile(PY_FILE), f"Python script {PY_FILE} does not exist."
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."

def test_log_file_content():
    """Verify the benchmark log file contains the expected success string."""
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} missing."
    with open(LOG_FILE, "r") as f:
        content = f.read()

    expected_str = "Result Match: True | C_Faster: True"
    assert expected_str in content, f"Log file does not contain the expected string: '{expected_str}'. Found: {content}"

def test_c_library_correctness():
    """Verify the compiled C shared library implements the algorithm correctly."""
    assert os.path.isfile(SO_FILE), f"Shared library {SO_FILE} missing."

    try:
        lib = ctypes.CDLL(SO_FILE)
    except Exception as e:
        pytest.fail(f"Failed to load shared library {SO_FILE}: {e}")

    try:
        lib.verify_token.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        lib.verify_token.restype = ctypes.c_longlong
    except AttributeError:
        pytest.fail("Function 'verify_token' not found in the shared library.")

    token = b"test_token"
    secret = b"my_secret"
    iterations = 500

    try:
        result = lib.verify_token(token, secret, iterations)
    except Exception as e:
        pytest.fail(f"Error calling verify_token from shared library: {e}")

    # Expected pure Python calculation
    py_result = 0
    token_len = len(token)
    secret_len = len(secret)

    if token_len > 0 and secret_len > 0:
        for _ in range(iterations):
            for i in range(token_len):
                s_char = secret[i % secret_len]
                val = (token[i] ^ s_char) * (i + 1)
                py_result = (py_result + val) % 1000003

    assert result == py_result, f"C library returned {result}, but expected {py_result}"

def test_c_library_edge_cases():
    """Verify the compiled C shared library handles edge cases correctly."""
    assert os.path.isfile(SO_FILE), f"Shared library {SO_FILE} missing."
    lib = ctypes.CDLL(SO_FILE)
    lib.verify_token.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    lib.verify_token.restype = ctypes.c_longlong

    # Empty token
    assert lib.verify_token(b"", b"secret", 10) == 0, "Expected 0 for empty token"
    # Empty secret
    assert lib.verify_token(b"token", b"", 10) == 0, "Expected 0 for empty secret"
    # Zero iterations
    assert lib.verify_token(b"token", b"secret", 0) == 0, "Expected 0 for 0 iterations"
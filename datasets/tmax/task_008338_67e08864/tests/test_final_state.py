# test_final_state.py

import os
import json
import ctypes
import pytest

APP_DIR = "/home/user/app"
REQUESTS_FILE = os.path.join(APP_DIR, "requests.json")
RESULTS_FILE = os.path.join(APP_DIR, "results.log")
LIBCALC_SO = os.path.join(APP_DIR, "libcalc.so")
API_PY = os.path.join(APP_DIR, "api.py")

def compute_expected_results(requests_path):
    with open(requests_path, 'r') as f:
        requests = json.load(f)

    user_counts = {}
    expected_lines = []

    for req in requests:
        user = req['user']
        data = req['data']

        is_valid = data.isalnum()

        user_counts[user] = user_counts.get(user, 0) + 1
        is_rate_limited = user_counts[user] > 2

        if is_valid and not is_rate_limited:
            truncated_data = data[:10]
            res = sum(ord(c) for c in truncated_data)
            expected_lines.append(f"USER:{user} STATUS:ACCEPTED RESULT:{res}")
        else:
            expected_lines.append(f"USER:{user} STATUS:REJECTED RESULT:NONE")

    return expected_lines

def test_results_log_content():
    assert os.path.exists(RESULTS_FILE), f"The file {RESULTS_FILE} was not created."

    expected_lines = compute_expected_results(REQUESTS_FILE)

    with open(RESULTS_FILE, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in results.log, but found {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1} in results.log.\nExpected: {expected}\nActual:   {actual}"

def test_libcalc_memory_safety_and_truncation():
    assert os.path.exists(LIBCALC_SO), f"{LIBCALC_SO} does not exist. Was it recompiled?"

    try:
        lib = ctypes.CDLL(LIBCALC_SO)
        lib.process_data.argtypes = [ctypes.c_char_p]
        lib.process_data.restype = ctypes.c_int
    except Exception as e:
        pytest.fail(f"Failed to load {LIBCALC_SO}: {e}")

    # Test with a string exactly 10 characters
    exact_str = b"1234567890"
    expected_exact = sum(c for c in exact_str)
    res_exact = lib.process_data(exact_str)
    assert res_exact == expected_exact, f"Expected {expected_exact} for 10-char string, got {res_exact}"

    # Test with a very long string to ensure no buffer overflow and proper truncation
    long_str = b"A" * 200
    expected_long = sum(c for c in (b"A" * 10))
    try:
        res_long = lib.process_data(long_str)
    except Exception as e:
        pytest.fail(f"Calling process_data with a long string crashed, memory safety issue not fixed: {e}")

    assert res_long == expected_long, (
        f"Expected {expected_long} for long string (truncated to 10), got {res_long}. "
        "Truncation logic is incorrect."
    )

def test_api_py_is_python3():
    assert os.path.exists(API_PY), f"{API_PY} does not exist."

    # Attempt to compile the file using Python 3's built-in compile()
    with open(API_PY, 'r') as f:
        source = f.read()

    try:
        compile(source, API_PY, 'exec')
    except SyntaxError as e:
        pytest.fail(f"{API_PY} is not valid Python 3 code. SyntaxError: {e}")
# test_final_state.py

import sys
import os
import ctypes
import pytest

sys.path.insert(0, "/home/user/math-api")

def test_c_library_fixed():
    so_path = "/home/user/math-api/libmathcore.so"
    assert os.path.exists(so_path), "libmathcore.so not found. Did you run make?"

    try:
        math_core = ctypes.CDLL(so_path)
    except OSError as e:
        pytest.fail(f"Failed to load libmathcore.so: {e}")

    math_core.fast_mod.argtypes = [ctypes.c_uint64, ctypes.c_uint64]
    math_core.fast_mod.restype = ctypes.c_uint64

    # 10 % 3 = 1
    res = math_core.fast_mod(10, 3)
    assert res == 1, f"fast_mod(10, 3) returned {res}, expected 1. The inline assembly is likely still returning the quotient or is mapped incorrectly."

    # 100 % 7 = 2
    res2 = math_core.fast_mod(100, 7)
    assert res2 == 2, f"fast_mod(100, 7) returned {res2}, expected 2."

def test_flask_app_validation_and_rate_limit():
    try:
        from app import app
    except ImportError as e:
        pytest.fail(f"Could not import app.py: {e}")

    app.testing = True
    client = app.test_client()

    # Validation tests
    # valid
    resp = client.get('/mod?a=10&m=3')
    assert resp.status_code == 200, "Expected 200 OK for valid request"
    assert resp.json == {"result": 1}, "Expected correct JSON result"

    # invalid: missing parameter
    resp = client.get('/mod?a=10')
    assert resp.status_code == 400, "Expected 400 for missing 'm' parameter"
    assert resp.json == {"error": "Invalid input"}, "Expected exact error JSON: {'error': 'Invalid input'}"

    # invalid: negative a
    resp = client.get('/mod?a=-5&m=3')
    assert resp.status_code == 400, "Expected 400 for negative 'a'"
    assert resp.json == {"error": "Invalid input"}, "Expected exact error JSON: {'error': 'Invalid input'}"

    # invalid: zero m
    resp = client.get('/mod?a=10&m=0')
    assert resp.status_code == 400, "Expected 400 for zero 'm'"
    assert resp.json == {"error": "Invalid input"}, "Expected exact error JSON: {'error': 'Invalid input'}"

    # invalid: non-integer
    resp = client.get('/mod?a=abc&m=3')
    assert resp.status_code == 400, "Expected 400 for non-integer input"
    assert resp.json == {"error": "Invalid input"}, "Expected exact error JSON: {'error': 'Invalid input'}"

    # Rate limiting test using a dedicated mock IP
    mock_ip = '10.99.99.99'
    for i in range(5):
        resp = client.get('/mod?a=10&m=3', environ_base={'REMOTE_ADDR': mock_ip})
        assert resp.status_code == 200, f"Expected 200 OK on request {i+1} before rate limit is hit"

    # The 6th request from the same IP should hit the rate limit
    resp = client.get('/mod?a=10&m=3', environ_base={'REMOTE_ADDR': mock_ip})
    assert resp.status_code == 429, "Expected 429 Too Many Requests for the 6th request within a minute"

def test_run_tests_script_and_report():
    script_path = "/home/user/math-api/run_tests.sh"
    assert os.path.exists(script_path), "run_tests.sh not found"
    assert os.access(script_path, os.X_OK), "run_tests.sh is not executable"

    report_path = "/home/user/math-api/test_report.log"
    assert os.path.exists(report_path), "test_report.log not found. Did the script run successfully and generate the file?"

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == "ALL TESTS PASSED", f"Expected test_report.log to contain exactly 'ALL TESTS PASSED', but got '{content}'"
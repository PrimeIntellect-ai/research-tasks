# test_final_state.py

import os
import ctypes
import math
import pytest

def test_libanomaly_exists():
    path = "/home/user/libanomaly.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist."

def test_c_backend_logic():
    path = "/home/user/libanomaly.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist."

    lib = ctypes.CDLL(path)
    assert hasattr(lib, 'compute_anomaly_score'), "Function compute_anomaly_score not found in libanomaly.so"

    lib.compute_anomaly_score.restype = ctypes.c_double
    lib.compute_anomaly_score.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]

    # Test [3.0, 4.0] -> RMS = sqrt((9+16)/2) = sqrt(12.5) = 3.5355339
    arr = (ctypes.c_double * 2)(3.0, 4.0)
    result = lib.compute_anomaly_score(arr, 2)
    expected = math.sqrt((3.0**2 + 4.0**2) / 2)
    assert math.isclose(result, expected, rel_tol=1e-5), f"Expected RMS approx {expected}, got {result}"

def test_merged_anomalies_exists_and_content():
    path = "/home/user/merged_anomalies.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist."

    # Must be readable as UTF-8
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        pytest.fail(f"{path} is not valid UTF-8.")

    expected_lines = [
        "SENS_C: 10.0000",
        "SENS_F: 10.0000",
        "SENS_B: 5.0662",
        "SENS_A: 2.1602",
        "SENS_D: 2.0000",
        "SENS_E: 0.0000"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, got {len(lines)}"

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual}'"

def test_test_results_log():
    path = "/home/user/test_results.log"
    assert os.path.isfile(path), f"Test results log {path} does not exist."

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    assert "OK" in content or "Ran" in content, f"Test results log does not indicate successful test execution. Content: {content}"
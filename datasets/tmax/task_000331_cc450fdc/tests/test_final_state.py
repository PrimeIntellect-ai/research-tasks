# test_final_state.py

import os
import pytest

def test_shared_library_exists():
    path = "/home/user/libmathapi.so"
    assert os.path.isfile(path), f"Shared library missing: {path}"
    assert os.access(path, os.R_OK), f"Shared library not readable: {path}"

def test_test_harness_c_exists():
    path = "/home/user/test_harness.c"
    assert os.path.isfile(path), f"Test harness source missing: {path}"

def test_test_harness_executable_exists():
    path = "/home/user/test_harness"
    assert os.path.isfile(path), f"Test harness executable missing: {path}"
    assert os.access(path, os.X_OK), f"Test harness is not executable: {path}"

def test_generate_urls_script_exists():
    path = "/home/user/generate_urls.sh"
    assert os.path.isfile(path), f"Generate URLs script missing: {path}"
    assert os.access(path, os.X_OK), f"Generate URLs script is not executable: {path}"

def test_sorted_results_log():
    path = "/home/user/sorted_results.log"
    assert os.path.isfile(path), f"Sorted results log missing: {path}"

    expected_lines = [
        "/api/add?a=10&b=20 = 30.00",
        "/api/add?a=10&b=5 = 15.00",
        "/api/add?a=12&b=6 = 18.00",
        "/api/add?a=14&b=7 = 21.00",
        "/api/add?a=16&b=8 = 24.00",
        "/api/add?a=18&b=9 = 27.00",
        "/api/add?a=1&b=2 = 3.00",
        "/api/add?a=20&b=10 = 30.00",
        "/api/add?a=2&b=1 = 3.00",
        "/api/add?a=2&b=4 = 6.00",
        "/api/add?a=3&b=6 = 9.00",
        "/api/add?a=4&b=2 = 6.00",
        "/api/add?a=4&b=8 = 12.00",
        "/api/add?a=5&b=10 = 15.00",
        "/api/add?a=6&b=12 = 18.00",
        "/api/add?a=6&b=3 = 9.00",
        "/api/add?a=7&b=14 = 21.00",
        "/api/add?a=8&b=16 = 24.00",
        "/api/add?a=8&b=4 = 12.00",
        "/api/add?a=9&b=18 = 27.00"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == 20, f"Expected exactly 20 lines in {path}, found {len(actual_lines)}"

    # Check that the set of lines is correct (ignoring sort order for this specific assertion)
    assert set(actual_lines) == set(expected_lines), "The generated results do not match the expected output values."

    # Check the exact sorted order
    assert actual_lines == expected_lines, f"The lines in {path} are not sorted correctly according to the expected output."
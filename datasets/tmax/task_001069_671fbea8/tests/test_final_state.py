# test_final_state.py

import os
import re
import subprocess
import ctypes
import pytest

LIB_PATH = "/home/user/librouter.so"
RESULTS_PATH = "/home/user/benchmark_results.txt"

def test_shared_library_exists():
    """Check that the shared library has been compiled and exists."""
    assert os.path.isfile(LIB_PATH), f"Shared library not found at {LIB_PATH}"

def test_symbol_export_no_mangling():
    """Check that parse_route is exported with C linkage (no C++ mangling)."""
    try:
        output = subprocess.check_output(["nm", "-D", LIB_PATH], text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run nm on {LIB_PATH}: {e}")

    # Look for the exact symbol parse_route
    # It should appear as ' T parse_route' or similar
    match = re.search(r'\b[A-Za-z]\s+parse_route\b', output)
    assert match is not None, "Symbol 'parse_route' not found or is mangled in the shared library."

def test_library_correctness():
    """Test the correctness of the parse_route function using ctypes."""
    try:
        lib = ctypes.CDLL(LIB_PATH)
    except Exception as e:
        pytest.fail(f"Failed to load shared library with ctypes: {e}")

    # Ensure the function exists
    assert hasattr(lib, "parse_route"), "Function parse_route not found in the shared library."

    path_buf = ctypes.create_string_buffer(256)
    query_buf = ctypes.create_string_buffer(256)

    # Test 1: With Query
    lib.parse_route(b"/users/123?active=true", path_buf, query_buf)
    assert path_buf.value == b"/users/123", f"Expected path '/users/123', got {path_buf.value}"
    assert query_buf.value == b"active=true", f"Expected query 'active=true', got {query_buf.value}"

    # Test 2: Without Query
    lib.parse_route(b"/healthcheck", path_buf, query_buf)
    assert path_buf.value == b"/healthcheck", f"Expected path '/healthcheck', got {path_buf.value}"
    assert query_buf.value == b"", f"Expected empty query, got {query_buf.value}"

def test_benchmark_results_format():
    """Check that the benchmark results file exists and has the correct format."""
    assert os.path.isfile(RESULTS_PATH), f"Benchmark results file not found at {RESULTS_PATH}"

    with open(RESULTS_PATH, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {RESULTS_PATH}, got {len(lines)}"

    assert lines[0] == "Route: /api/v2/items", f"Line 1 incorrect: {lines[0]}"
    assert lines[1] == "Query: category=books&sort=desc", f"Line 2 incorrect: {lines[1]}"

    time_match = re.match(r"^Time:\s+\d+\.\d+$", lines[2])
    assert time_match is not None, f"Line 3 incorrect format: {lines[2]}"
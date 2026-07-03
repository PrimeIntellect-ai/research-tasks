# test_final_state.py

import os
import ctypes
import re

PIPELINE_DIR = "/home/user/pipeline"

def test_libfilter_so_built_and_valid():
    so_path = os.path.join(PIPELINE_DIR, "libfilter.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built."

    # Try loading it to ensure it's a valid shared object
    try:
        lib = ctypes.CDLL(so_path)
    except OSError as e:
        assert False, f"Failed to load {so_path} as a shared library: {e}"

    assert hasattr(lib, "moving_average"), "libfilter.so does not export 'moving_average'"

def test_filter_cpp_memory_leak_fixed():
    cpp_path = os.path.join(PIPELINE_DIR, "filter.cpp")
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."
    with open(cpp_path, "r") as f:
        content = f.read()

    # The fix typically involves 'delete[] temp;' or removing 'new double[size]' entirely
    # Let's check if 'delete[] temp' is present, or if 'new double' is gone.
    has_new = "new double" in content
    has_delete = "delete[] temp" in content.replace(" ", "")

    assert not has_new or has_delete, "Memory leak in filter.cpp does not appear to be fixed."

def test_valgrind_log_shows_no_leaks():
    log_path = os.path.join(PIPELINE_DIR, "valgrind.log")
    assert os.path.isfile(log_path), f"Valgrind log {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()

    # Check for typical valgrind success messages
    success_indicators = [
        "All heap blocks were freed -- no leaks are possible",
        "definitely lost: 0 bytes"
    ]

    found_success = any(indicator in content for indicator in success_indicators)
    assert found_success, "valgrind.log does not indicate that the memory leak was fixed (0 bytes lost)."

def test_benchmark_result_exists_and_complete():
    res_path = os.path.join(PIPELINE_DIR, "benchmark_result.txt")
    assert os.path.isfile(res_path), f"Benchmark result {res_path} does not exist."
    with open(res_path, "r") as f:
        content = f.read()

    assert "Benchmark complete." in content, "benchmark_result.txt does not contain 'Benchmark complete.'"
    assert "C++ Time:" in content, "benchmark_result.txt does not contain C++ benchmark results."
    assert "Python Time:" in content, "benchmark_result.txt does not contain Python benchmark results."
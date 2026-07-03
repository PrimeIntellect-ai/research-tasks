# test_final_state.py
import os
import ctypes
import pytest

def test_project_structure():
    expected_dirs = [
        "/home/user/project/src",
        "/home/user/project/include",
        "/home/user/project/lib",
        "/home/user/project/tests",
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Expected directory {d} is missing."

def test_moved_files():
    hpp_path = "/home/user/project/include/string_history.hpp"
    cpp_path = "/home/user/project/src/string_history.cpp"
    assert os.path.isfile(hpp_path), f"File {hpp_path} is missing."
    assert os.path.isfile(cpp_path), f"File {cpp_path} is missing."

def test_c_api_cpp_exists():
    api_path = "/home/user/project/src/c_api.cpp"
    assert os.path.isfile(api_path), f"File {api_path} is missing."
    with open(api_path, "r") as f:
        content = f.read()
    assert "History_create" in content, "c_api.cpp does not seem to contain History_create."

def test_shared_library_exists_and_exports():
    lib_path = "/home/user/project/lib/libhistory.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} is missing."

    try:
        lib = ctypes.CDLL(lib_path)
    except Exception as e:
        pytest.fail(f"Failed to load {lib_path} with ctypes: {e}")

    assert hasattr(lib, "History_create"), "libhistory.so does not export History_create"
    assert hasattr(lib, "History_destroy"), "libhistory.so does not export History_destroy"
    assert hasattr(lib, "History_add"), "libhistory.so does not export History_add"
    assert hasattr(lib, "History_get"), "libhistory.so does not export History_get"

def test_python_test_script_exists():
    script_path = "/home/user/project/tests/test_ffi.py"
    assert os.path.isfile(script_path), f"Python test script {script_path} is missing."

def test_test_results_log():
    log_path = "/home/user/project/test_results.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did the test script run successfully?"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "ALL TESTS PASSED", f"Expected log file to contain 'ALL TESTS PASSED', but got '{content}'"
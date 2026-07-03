# test_final_state.py

import os
import re
import subprocess

def test_rust_lib_built():
    so_path = "/home/user/release_prep/rust_ffi/target/release/librust_ffi.so"
    assert os.path.isfile(so_path), f"Rust shared library not found at {so_path}. Did you build in release mode?"

def test_test_log_exists_and_passed():
    log_path = "/home/user/release_prep/test.log"
    assert os.path.isfile(log_path), f"Test log file not found at {log_path}. Did you redirect pytest output?"

    with open(log_path, "r") as f:
        content = f.read()

    # Allow for variations like "1 passed"
    assert re.search(r"1 passed", content), "The test.log does not indicate that 1 test passed."

def test_test_release_py_modified():
    py_path = "/home/user/release_prep/test_release.py"
    assert os.path.isfile(py_path), f"Python test file missing at {py_path}"

    with open(py_path, "r") as f:
        content = f.read()

    assert "Mock()" not in content, "The Mock object is still present in test_release.py."
    assert "ctypes.CDLL" in content, "ctypes.CDLL is not being used to load the shared library."
    assert "argtypes" in content, "argtypes is not configured for the function."
    assert "restype" in content, "restype is not configured for the function."

def test_rust_code_fixed():
    lib_rs_path = "/home/user/release_prep/rust_ffi/src/lib.rs"
    assert os.path.isfile(lib_rs_path), f"Rust source file missing at {lib_rs_path}"

    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "into_raw" in content, "The Rust code does not appear to use `into_raw` to pass ownership to C safely."

def test_pytest_runs_successfully():
    py_path = "/home/user/release_prep/test_release.py"
    # Run pytest on the file to ensure it actually works
    result = subprocess.run(["pytest", py_path], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest failed when run against {py_path}:\n{result.stdout}\n{result.stderr}"
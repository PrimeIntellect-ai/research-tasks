# test_final_state.py

import os
import pytest

def test_c_lib_compiled():
    c_lib_path = "/home/user/project/clib/libc_lib.so"
    assert os.path.exists(c_lib_path), f"C library {c_lib_path} was not compiled or is missing."

def test_rust_lib_compiled():
    rust_lib_path = "/home/user/project/rust_wrapper/target/release/librust_wrapper.so"
    assert os.path.exists(rust_lib_path), f"Rust library {rust_lib_path} was not compiled or is missing."

def test_rust_build_script_fixed():
    build_rs_path = "/home/user/project/rust_wrapper/build.rs"
    assert os.path.exists(build_rs_path), f"File {build_rs_path} is missing."
    with open(build_rs_path, "r") as f:
        content = f.read()
    assert "cargo:rustc-link-search=" in content, "build.rs does not contain the necessary 'cargo:rustc-link-search' directive to fix the linking issue."

def test_rust_lib_fixed():
    lib_rs_path = "/home/user/project/rust_wrapper/src/lib.rs"
    assert os.path.exists(lib_rs_path), f"File {lib_rs_path} is missing."
    with open(lib_rs_path, "r") as f:
        content = f.read()
    assert "into_raw" in content, "lib.rs does not seem to fix the borrow checker bug (missing 'into_raw()')."

def test_python_script_exists():
    py_script_path = "/home/user/project/test_ffi.py"
    assert os.path.exists(py_script_path), f"Python test script {py_script_path} is missing."

def test_diff_output_correct():
    diff_path = "/home/user/project/diff.txt"
    assert os.path.exists(diff_path), f"Diff output file {diff_path} is missing."

    with open(diff_path, "r") as f:
        diff_content = f.read()

    assert diff_content.strip() == "", "Diff output should be empty because the merged and sorted list should match expected.txt exactly."
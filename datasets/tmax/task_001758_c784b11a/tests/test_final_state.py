# test_final_state.py

import os
import pytest

def test_rust_library_built():
    """Verify that the Rust project was successfully built as a shared library."""
    lib_path = "/home/user/test_env/rust_src/target/debug/libversion_check.so"
    assert os.path.isfile(lib_path), f"Expected compiled Rust shared library at {lib_path}, but it is missing. Did you run 'cargo build'?"

def test_go_test_output_exists():
    """Verify that the test output log was created."""
    log_path = "/home/user/test_output.log"
    assert os.path.isfile(log_path), f"Expected Go test output log at {log_path}, but it is missing."

def test_go_test_passed():
    """Verify that the Go test suite was run successfully and passed."""
    log_path = "/home/user/test_output.log"
    assert os.path.isfile(log_path), f"Cannot check test results because {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "PASS" in content, "The test output log does not contain 'PASS'. Ensure the tests ran successfully."
    assert "TestVersionParser" in content, "The test output log does not indicate that 'TestVersionParser' was run."
    assert "PASS: TestVersionParser" in content, "The test output log does not contain the expected successful test pass message ('PASS: TestVersionParser')."
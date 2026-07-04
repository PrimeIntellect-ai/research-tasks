# test_final_state.py

import os
import pytest

def test_polygen_cpp_exists():
    """Test that the polygen.cpp source file exists."""
    path = "/home/user/polybuild/polygen.cpp"
    assert os.path.isfile(path), f"Source file {path} is missing."

def test_polygen_binary_executable():
    """Test that the polygen binary exists and is executable."""
    path = "/home/user/polybuild/polygen"
    assert os.path.isfile(path), f"Binary file {path} is missing."
    assert os.access(path, os.X_OK), f"Binary file {path} is not executable."

def test_makefile_exists():
    """Test that the Makefile was generated."""
    path = "/home/user/polybuild/Makefile"
    assert os.path.isfile(path), f"Generated file {path} is missing."

def test_build_success_log():
    """Test that the integration test passed and created the success log."""
    path = "/home/user/polybuild/build_success.log"
    assert os.path.isfile(path), f"Log file {path} is missing. Did 'make all' run successfully?"

    with open(path, "r") as f:
        content = f.read()

    assert "INTEGRATION_TEST_PASSED" in content, f"Expected 'INTEGRATION_TEST_PASSED' in {path}, but found: {content}"
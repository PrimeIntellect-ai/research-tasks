# test_final_state.py

import os
import sys
import importlib.util

def test_file_existence():
    """Verify that all required files and directories exist."""
    required_files = [
        "/home/user/rust_validator/Cargo.toml",
        "/home/user/rust_validator/target/release/librust_validator.so",
        "/home/user/py3_wrapper.py",
        "/home/user/test_validator.py",
        "/home/user/test_results.log",
    ]
    for file_path in required_files:
        assert os.path.isfile(file_path), f"Required file missing: {file_path}"

def test_log_file_verification():
    """Verify that the test results log indicates a successful test run."""
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pytest usually outputs something like "1 passed" or "X passed" at the end
    assert "passed" in content, "Log file does not indicate a passed test run. Looked for 'passed'."
    assert "failed" not in content.lower() or "0 failed" in content.lower(), "Log file indicates there were failed tests."

def test_functional_py3_wrapper():
    """Verify that the compute_signature function works correctly."""
    wrapper_path = "/home/user/py3_wrapper.py"
    assert os.path.isfile(wrapper_path), f"Wrapper file missing: {wrapper_path}"

    # Import the module dynamically
    spec = importlib.util.spec_from_file_location("py3_wrapper", wrapper_path)
    assert spec is not None, "Could not load py3_wrapper.py"
    py3_wrapper = importlib.util.module_from_spec(spec)
    sys.modules["py3_wrapper"] = py3_wrapper
    spec.loader.exec_module(py3_wrapper)

    assert hasattr(py3_wrapper, "compute_signature"), "compute_signature function is missing in py3_wrapper.py"
    compute_signature = py3_wrapper.compute_signature

    # Test values
    token_id = 123456789
    salt = 987654321
    expected = ((token_id ^ salt) * 11400714819323198485) % (2**64)
    result = compute_signature(token_id, salt)
    assert result == expected, f"Expected {expected}, got {result} for token_id={token_id}, salt={salt}"

    # Boundary test
    token_id = 0xFFFFFFFFFFFFFFFF
    salt = 0xFFFFFFFFFFFFFFFF
    expected = 0
    result = compute_signature(token_id, salt)
    assert result == expected, f"Expected {expected}, got {result} for token_id={token_id}, salt={salt}"
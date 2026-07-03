# test_final_state.py

import os
import subprocess
import pytest

def test_shared_library_compiled():
    """Verify that libratelimit.so was compiled."""
    assert os.path.isfile("/home/user/src/libratelimit.so"), "/home/user/src/libratelimit.so does not exist. Did you compile the library?"

def test_shared_library_abi():
    """Verify that allow_request is exported with C ABI (no mangling)."""
    so_path = "/home/user/src/libratelimit.so"
    assert os.path.isfile(so_path), f"{so_path} missing."

    # Use nm to check for the unmangled symbol
    result = subprocess.run(["nm", "-D", so_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run nm on the shared library."

    # We should see 'allow_request' in the output, not e.g., '_Z13allow_requestjj'
    symbols = result.stdout.splitlines()
    found_unmangled = any(line.endswith(" allow_request") for line in symbols)
    assert found_unmangled, "Could not find unmangled 'allow_request' in the shared library. Did you add extern \"C\"?"

def test_python_script_exists():
    """Verify that the test_api.py script exists."""
    assert os.path.isfile("/home/user/test_api.py"), "/home/user/test_api.py does not exist."

def test_api_results_log():
    """Verify that the api_results.log matches the expected output."""
    log_path = "/home/user/api_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you run your Python script?"

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "ACCEPTED: 12:GET /api/v1/users",
        "ACCEPTED: 12:POST /api/v1/data",
        "ACCEPTED: 45:GET /status",
        "REJECTED: 12:DELETE /api/v1/users/1",
        "ACCEPTED: 45:POST /login",
        "REJECTED: 45:GET /dashboard",
        "REJECTED: 12:GET /retry"
    ]

    assert actual_lines == expected_lines, "The contents of api_results.log do not match the expected output. Check your rate limiting, logging format, and malformed line handling."
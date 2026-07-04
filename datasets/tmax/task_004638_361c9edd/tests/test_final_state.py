# test_final_state.py

import os
import sys
import zlib
import subprocess
import importlib.util

def test_result_file():
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"File not found: {result_path}"

    with open(result_path, "r") as f:
        content = f.read().strip()

    expected_checksum = zlib.crc32(b"MOBILE_BUILD_PIPELINE_STABLE")
    assert content == str(expected_checksum), f"Expected result.txt to contain '{expected_checksum}', but found '{content}'"

def test_checksum_wrapper():
    wrapper_path = "/home/user/checksum_wrapper.py"
    assert os.path.exists(wrapper_path), f"File not found: {wrapper_path}"

    # Import the module dynamically
    spec = importlib.util.spec_from_file_location("checksum_wrapper", wrapper_path)
    checksum_wrapper = importlib.util.module_from_spec(spec)
    sys.modules["checksum_wrapper"] = checksum_wrapper
    try:
        spec.loader.exec_module(checksum_wrapper)
    except Exception as e:
        assert False, f"Failed to import checksum_wrapper.py: {e}"

    assert hasattr(checksum_wrapper, "get_checksum"), "get_checksum function is missing from checksum_wrapper.py"

    try:
        test_val = b"test"
        result = checksum_wrapper.get_checksum(test_val)
    except Exception as e:
        assert False, f"Calling get_checksum failed: {e}. The ctypes FFI might still be buggy."

    expected = zlib.crc32(test_val)
    assert result == expected, f"get_checksum(b'test') returned {result}, expected {expected}"

def test_unit_test_script():
    test_script_path = "/home/user/test_checksum.py"
    assert os.path.exists(test_script_path), f"File not found: {test_script_path}"

    # Run the test script
    result = subprocess.run(
        [sys.executable, test_script_path],
        cwd="/home/user",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"test_checksum.py failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
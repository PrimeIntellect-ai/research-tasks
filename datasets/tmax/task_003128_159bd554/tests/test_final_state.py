# test_final_state.py

import os
import json
import pytest

def py_checksum(data: bytes) -> int:
    hash_val = 0x811c9dc5
    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * 0x01000193) & 0xFFFFFFFF
    return hash_val

def test_shared_library_exists():
    """Test that the C library was compiled into a shared object."""
    assert os.path.isfile("/home/user/libmath_lib.so"), "/home/user/libmath_lib.so is missing. Did you compile the C code?"

def test_results_json_exists():
    """Test that the app.py script successfully generated the results.json file."""
    assert os.path.isfile("/home/user/results.json"), "/home/user/results.json is missing. Did you run app.py?"

def test_results_json_content():
    """Test that results.json contains the correct checksum and benchmarking result."""
    assert os.path.isfile("/home/user/payload.bin"), "payload.bin is missing."
    assert os.path.isfile("/home/user/results.json"), "results.json is missing."

    with open("/home/user/payload.bin", "rb") as f:
        data = f.read()

    expected_checksum = py_checksum(data)

    with open("/home/user/results.json", "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    assert "checksum" in results, "results.json is missing the 'checksum' key."
    assert results["checksum"] == expected_checksum, f"Checksum in results.json ({results['checksum']}) does not match the expected value ({expected_checksum}). The FFI binding might still be truncating data or using wrong types."

    assert "c_faster_than_py" in results, "results.json is missing the 'c_faster_than_py' key."
    # The C version should generally be faster than the pure Python version.
    assert results["c_faster_than_py"] is True, "c_faster_than_py is not true. The C implementation should be faster."

def test_app_py_modifications():
    """Test that app.py was modified to fix the ABI mismatch."""
    assert os.path.isfile("/home/user/app.py"), "app.py is missing."
    with open("/home/user/app.py", "r") as f:
        content = f.read()

    # Check that c_size_t and c_uint32 are used, or equivalent fixes for 64-bit compatibility
    assert "c_size_t" in content, "app.py does not seem to use ctypes.c_size_t for the length argument."
    assert "c_uint32" in content, "app.py does not seem to use ctypes.c_uint32 for the return type."
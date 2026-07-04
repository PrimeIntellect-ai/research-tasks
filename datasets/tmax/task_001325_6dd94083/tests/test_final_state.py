# test_final_state.py

import os
import ctypes
import pytest

PROJECT_DIR = "/home/user/project"

def test_libchecksum_so_built():
    """Verify that libchecksum.so was built successfully."""
    so_path = os.path.join(PROJECT_DIR, "libchecksum.so")
    assert os.path.isfile(so_path), f"{so_path} does not exist. Did you run make and fix the Makefile?"

    # Try to load it to ensure it's a valid shared library
    try:
        lib = ctypes.CDLL(so_path)
    except OSError as e:
        pytest.fail(f"Failed to load {so_path}. Is it a valid shared library compiled with -fPIC and -shared? Error: {e}")

    assert hasattr(lib, "compute_checksum"), "compute_checksum function not found in libchecksum.so"

def test_protobuf_compiled():
    """Verify that message.proto was compiled to Python."""
    pb2_path = os.path.join(PROJECT_DIR, "message_pb2.py")
    assert os.path.isfile(pb2_path), f"{pb2_path} does not exist. Did you compile message.proto with protoc?"

def test_run_test_script_exists():
    """Verify that the test script run_test.py exists."""
    script_path = os.path.join(PROJECT_DIR, "run_test.py")
    assert os.path.isfile(script_path), f"{script_path} does not exist."

def test_checksum_output():
    """Verify that checksum_out.txt exists and contains the correct value."""
    out_path = os.path.join(PROJECT_DIR, "checksum_out.txt")
    assert os.path.isfile(out_path), f"{out_path} does not exist. Did your script write the output?"

    with open(out_path, "r") as f:
        content = f.read().strip()

    assert content == "3211", f"Expected checksum '3211', but found '{content}' in {out_path}."
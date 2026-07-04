# test_final_state.py

import os
import glob
import pytest

WORKSPACE = "/home/user/sec_ws"

def test_setup_py_fixed():
    setup_path = os.path.join(WORKSPACE, "setup.py")
    assert os.path.isfile(setup_path), f"setup.py is missing at {setup_path}"
    with open(setup_path, "r") as f:
        content = f.read()
    assert "fast_auth_ext" not in content, "setup.py still contains the misconfigured module name 'fast_auth_ext'."
    assert "Extension('fast_auth'" in content.replace('"', "'"), "setup.py does not define the correct Extension name 'fast_auth'."

def test_protobuf_compiled():
    pb2_path = os.path.join(WORKSPACE, "auth_pb2.py")
    assert os.path.isfile(pb2_path), f"Compiled protobuf file auth_pb2.py is missing at {pb2_path}. Did you compile it?"

def test_c_extension_fixed():
    c_path = os.path.join(WORKSPACE, "src", "deserializer.c")
    assert os.path.isfile(c_path), f"C extension file missing at {c_path}"
    with open(c_path, "r") as f:
        content = f.read()

    assert "Invalid token length" in content, "C file does not contain the expected error message 'Invalid token length' for the bounds check."
    assert "PyExc_ValueError" in content, "C file does not raise a ValueError for the bounds check."

def test_extension_compiled():
    # Look for the compiled shared object file
    so_files = glob.glob(os.path.join(WORKSPACE, "fast_auth*.so"))
    assert len(so_files) > 0, "Compiled C extension (fast_auth*.so) not found in the workspace. Did you run setup.py build_ext --inplace?"

def test_result_log():
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"Result log missing at {log_path}. Did you run test_server.py and redirect the output?"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "SUCCESS_HASH_8F92A1B" in content, f"Expected success hash not found in {log_path}."
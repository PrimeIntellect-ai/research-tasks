# test_final_state.py
import os
import subprocess
import ctypes
import pytest

def test_result_log_contents():
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"The file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "user_id: 42, is_admin: 1", f"Expected 'user_id: 42, is_admin: 1', but got '{content}'"

def test_libsession_exports_function():
    lib_path = "/home/user/src/libsession.so"
    assert os.path.isfile(lib_path), f"The compiled library {lib_path} does not exist."

    # Check export using nm
    result = subprocess.run(["nm", "-D", lib_path], capture_output=True, text=True)
    assert "parse_session" in result.stdout, "The function 'parse_session' is not exported in libsession.so."

def test_memory_safety_no_segfault():
    # We run a small python script in a subprocess to avoid crashing the pytest runner
    # if the C code still has a buffer overflow.
    script = """
import ctypes
import sys

class Session(ctypes.Structure):
    _fields_ = [
        ("user_id", ctypes.c_int),
        ("username", ctypes.c_char * 16),
        ("is_admin", ctypes.c_int)
    ]

try:
    lib = ctypes.CDLL("/home/user/src/libsession.so")
    lib.parse_session.argtypes = [ctypes.c_char_p, ctypes.POINTER(Session)]
    lib.parse_session.restype = ctypes.c_int

    sess = Session()
    # Very long payload to trigger buffer overflow if not fixed
    payload = b"99,superlongusernamewhichdefinitelyexceeds32bytesandwillcrashifstrcpyisused,1"
    res = lib.parse_session(payload, ctypes.byref(sess))

    if sess.user_id == 99 and sess.is_admin == 1:
        sys.exit(0)
    else:
        sys.exit(2)
except Exception as e:
    sys.exit(1)
"""
    result = subprocess.run(["python3", "-c", script], capture_output=True)
    if result.returncode == -11:
        pytest.fail("The C library segfaulted when parsing a long payload. The buffer overflow is not fixed.")
    elif result.returncode == 1:
        pytest.fail("An exception occurred when calling the C library from Python.")
    elif result.returncode == 2:
        pytest.fail("The C library parsed the long payload without crashing, but the parsed values were incorrect.")
    elif result.returncode != 0:
        pytest.fail(f"The C library test failed with return code {result.returncode}.")
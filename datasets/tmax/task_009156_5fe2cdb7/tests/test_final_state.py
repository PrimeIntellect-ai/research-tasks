# test_final_state.py

import os
import ctypes
import struct

def test_libsemver_exists_and_is_elf():
    lib_path = "/home/user/app/libsemver.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist. Did you run make?"

    with open(lib_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{lib_path} is not a valid ELF file. Check your Makefile compilation flags."

def test_test_result_log_exists_and_passed():
    log_path = "/home/user/test_result.log"
    assert os.path.isfile(log_path), f"Test log {log_path} does not exist. Did you redirect the pytest output?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "1 passed" in content or "passed" in content.lower(), f"Test log does not indicate success. Content:\n{content}"

def test_c_logic_correctness():
    lib_path = "/home/user/app/libsemver.so"
    assert os.path.isfile(lib_path), "Cannot test C logic because libsemver.so is missing."

    lib = ctypes.CDLL(lib_path)
    lib.is_greater_or_equal.argtypes = [ctypes.c_char_p, ctypes.c_uint16, ctypes.c_uint16, ctypes.c_uint16]
    lib.is_greater_or_equal.restype = ctypes.c_int

    test_cases = [
        ((1, 0, 0), (1, 0, 0), 1),
        ((2, 0, 0), (1, 9, 9), 1),
        ((1, 2, 0), (1, 1, 9), 1),
        ((1, 1, 2), (1, 1, 1), 1),
        ((1, 1, 1), (1, 1, 2), 0),
        ((1, 1, 9), (1, 2, 0), 0),
        ((1, 9, 9), (2, 0, 0), 0),
    ]

    for v1, v2, expected in test_cases:
        raw_bytes = struct.pack('<HHH', v1[0], v1[1], v1[2])
        res = lib.is_greater_or_equal(raw_bytes, v2[0], v2[1], v2[2])
        assert res == expected, f"Logic error: {v1} >= {v2} should be {expected}, but got {res}"
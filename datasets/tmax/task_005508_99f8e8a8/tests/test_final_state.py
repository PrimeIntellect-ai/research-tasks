# test_final_state.py

import os
import pytest

def test_libring_so_exists():
    so_path = "/home/user/sysproj/libring.so"
    assert os.path.isfile(so_path), f"{so_path} does not exist."

    # Check if it's an ELF file (shared object)
    with open(so_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{so_path} is not a valid ELF file."

def test_test_suite_py_exists_and_uses_ctypes():
    py_path = "/home/user/sysproj/test_suite.py"
    assert os.path.isfile(py_path), f"{py_path} does not exist."

    with open(py_path, "r") as f:
        content = f.read()
        assert "ctypes" in content, f"{py_path} does not import or use ctypes."
        assert "rb_init" in content, f"{py_path} does not call rb_init."
        assert "rb_push" in content, f"{py_path} does not call rb_push."
        assert "rb_pop" in content, f"{py_path} does not call rb_pop."
        assert "rb_dump" in content, f"{py_path} does not call rb_dump."

def test_test_results_log_content():
    log_path = "/home/user/sysproj/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()
        assert "10" in content, f"{log_path} does not contain the popped value 10."
        assert "RingBuffer Dump" in content, f"{log_path} does not contain 'RingBuffer Dump'."

def test_fix_patch_exists_and_contents():
    patch_path = "/home/user/sysproj/fix.patch"
    assert os.path.isfile(patch_path), f"{patch_path} does not exist."

    with open(patch_path, "r") as f:
        content = f.read()

        # Check diff headers
        assert "Makefile" in content, "Patch does not contain changes for Makefile."
        assert "libring.c" in content, "Patch does not contain changes for libring.c."

        # Check for -fPIC addition
        assert "-fPIC" in content or "-fpic" in content, "Patch does not show the addition of -fPIC to Makefile."

        # Check for conditional compilation logic in libring.c
        assert "DEBUG_MODE" in content, "Patch does not show the usage of DEBUG_MODE in libring.c."
        assert "RingBuffer Dump" in content, "Patch does not show the print statement in libring.c."
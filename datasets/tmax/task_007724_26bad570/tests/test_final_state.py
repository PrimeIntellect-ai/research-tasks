# test_final_state.py

import os
import re
import pytest

def test_success_log_exists_and_correct():
    log_path = "/home/user/py_ext/success.log"
    assert os.path.isfile(log_path), f"Success log file {log_path} is missing. Did you run the tests and redirect the output?"

    with open(log_path, "r") as f:
        content = f.read()

    assert content.strip() == "ALL TESTS PASSED", f"Expected success.log to contain exactly 'ALL TESTS PASSED', but got: {content}"

def test_fast_req_conditional_compilation():
    c_file_path = "/home/user/py_ext/fast_req.c"
    assert os.path.isfile(c_file_path), f"File {c_file_path} is missing."

    with open(c_file_path, "r") as f:
        content = f.read()

    assert "#if PY_MAJOR_VERSION >= 3" in content, "Missing '#if PY_MAJOR_VERSION >= 3' macro in fast_req.c"
    assert "PyUnicode_AsUTF8" in content, "Missing 'PyUnicode_AsUTF8' call for Python 3 logic in fast_req.c"
    assert "PyString_AsString" in content, "Missing 'PyString_AsString' call for Python 2 logic in fast_req.c"

def test_fast_req_memory_safety():
    c_file_path = "/home/user/py_ext/fast_req.c"
    assert os.path.isfile(c_file_path), f"File {c_file_path} is missing."

    with open(c_file_path, "r") as f:
        content = f.read()

    # Check for off-by-one fix (len + 1)
    assert re.search(r"malloc\s*\(\s*len\s*\+\s*1\s*\)", content), "Off-by-one error not fixed: could not find malloc(len + 1) in fast_req.c"

    # Check for memory leak fix (free)
    assert re.search(r"free\s*\(\s*buffer\s*\)", content), "Memory leak not fixed: could not find free(buffer) in error path of fast_req.c"

def test_migration_patch_exists_and_valid():
    patch_path = "/home/user/py_ext/migration.patch"
    assert os.path.isfile(patch_path), f"Patch file {patch_path} is missing."

    with open(patch_path, "r") as f:
        content = f.read()

    assert content.startswith("--- "), "Patch file does not appear to be a valid unified diff (should start with '--- ')."
    assert "\n+++ " in content, "Patch file does not appear to be a valid unified diff (missing '+++ ')."
    assert "fast_req.c" in content, "Patch file doesn't seem to reference fast_req.c."
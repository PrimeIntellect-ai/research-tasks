# test_final_state.py
import os
import pytest

def test_run_log_contents():
    log_path = "/home/user/run.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run the evaluation steps?"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {log_path}, found {len(lines)}."
    assert lines[0] == "-999", f"Expected first line to be '-999' (lite mode), but got '{lines[0]}'."
    assert lines[1] == "5", f"Expected second line to be '5' (full mode), but got '{lines[1]}'."

def test_c_math_c_updated():
    c_path = "/home/user/math_extension/c_math.c"
    assert os.path.isfile(c_path), f"File {c_path} does not exist."

    with open(c_path, "r") as f:
        content = f.read()

    assert "PyModuleDef" in content, "c_math.c does not appear to use PyModuleDef for Python 3 migration."
    assert "PyModule_Create" in content, "c_math.c does not appear to use PyModule_Create for Python 3 migration."
    assert "PyLong_FromLong" in content, "c_math.c does not appear to use PyLong_FromLong for Python 3 migration."
    assert "LITE_MODE" in content, "c_math.c does not contain logic for LITE_MODE."

def test_setup_py_updated():
    setup_path = "/home/user/math_extension/setup.py"
    assert os.path.isfile(setup_path), f"File {setup_path} does not exist."

    with open(setup_path, "r") as f:
        content = f.read()

    assert "BUILD_MODE" in content, "setup.py does not check the BUILD_MODE environment variable."
    assert "LITE_MODE" in content, "setup.py does not appear to add LITE_MODE to compiler arguments."
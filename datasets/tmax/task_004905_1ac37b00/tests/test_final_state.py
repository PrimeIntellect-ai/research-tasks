# test_final_state.py
import os
import pytest

def test_shared_libraries_exist():
    lib_v1 = "/home/user/lib/libdata.so.1"
    lib_v2 = "/home/user/lib/libdata.so.2"

    assert os.path.exists(lib_v1), f"Shared library missing: {lib_v1}"
    assert os.path.isfile(lib_v1), f"Expected a file at {lib_v1}"

    assert os.path.exists(lib_v2), f"Shared library missing: {lib_v2}"
    assert os.path.isfile(lib_v2), f"Expected a file at {lib_v2}"

def test_app_script_exists():
    app_path = "/home/user/app.py"
    assert os.path.exists(app_path), f"Python script missing: {app_path}"
    assert os.path.isfile(app_path), f"Expected a file at {app_path}"

def test_result_v1_contents():
    result_path = "/home/user/result_v1.txt"
    assert os.path.exists(result_path), f"Result file missing: {result_path}"

    with open(result_path, "r") as f:
        content = f.read()

    expected = "UftuTusjoh234\n"
    assert content == expected, f"Incorrect content in {result_path}. Expected {repr(expected)}, got {repr(content)}"

def test_result_v2_contents():
    result_path = "/home/user/result_v2.txt"
    assert os.path.exists(result_path), f"Result file missing: {result_path}"

    with open(result_path, "r") as f:
        content = f.read()

    expected = "VguvUvtkpi345\n"
    assert content == expected, f"Incorrect content in {result_path}. Expected {repr(expected)}, got {repr(content)}"
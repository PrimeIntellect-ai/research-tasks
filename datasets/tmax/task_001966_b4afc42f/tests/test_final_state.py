# test_final_state.py

import os
import json
import pytest

def test_c_source_exists_and_contains_fast_mode():
    c_file = "/home/user/counter.c"
    assert os.path.exists(c_file), f"{c_file} does not exist."
    with open(c_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "FAST_MODE" in content, f"{c_file} does not contain 'FAST_MODE'."

def test_shared_library_exists():
    so_file = "/home/user/libcounter.so"
    assert os.path.exists(so_file), f"{so_file} does not exist."
    assert os.path.isfile(so_file), f"{so_file} is not a file."

def test_python_script_exists_and_uses_ctypes():
    py_file = "/home/user/migrate.py"
    assert os.path.exists(py_file), f"{py_file} does not exist."
    with open(py_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "ctypes" in content, f"{py_file} does not import or use 'ctypes'."

def test_result_txt_contents():
    result_file = "/home/user/result.txt"
    assert os.path.exists(result_file), f"{result_file} does not exist."

    with open(result_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["100", "200", "-5", "999", "42"]
    assert lines == expected, f"Contents of {result_file} do not match the expected top 5 integers. Expected {expected}, got {lines}."

def test_benchmark_json_contents():
    json_file = "/home/user/benchmark.json"
    assert os.path.exists(json_file), f"{json_file} does not exist."

    with open(json_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_file} does not contain valid JSON.")

    expected_data = {"status": "success", "language": "python3+C"}
    assert data == expected_data, f"Contents of {json_file} do not match expected JSON. Expected {expected_data}, got {data}."
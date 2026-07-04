# test_final_state.py
import os
import pytest

def test_client_patched():
    path = "/home/user/client.py"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert 'print("Running client...")' in content, f"{path} was not patched correctly (missing Python 3 print statement)."
    assert 'print "Running client..."' not in content, f"{path} still contains Python 2 print statement."

def test_evaluator_so_exists():
    path = "/home/user/evaluator.so"
    assert os.path.isfile(path), f"Shared library {path} was not created."

def test_server_py_exists():
    path = "/home/user/server.py"
    assert os.path.isfile(path), f"Server script {path} was not created."

def test_output_correct():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file {path} was not created."

    expected_results = ["8", "20", "15", "10", "26"]

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_results, f"Contents of {path} do not match the expected results. Got {lines}, expected {expected_results}."
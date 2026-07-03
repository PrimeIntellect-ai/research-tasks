# test_final_state.py

import os
import re
import pytest

def test_venv_exists():
    venv_python = "/home/user/waf/venv/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment Python executable not found at {venv_python}. Did you create the venv?"

def test_protobuf_generated():
    pb2_file = "/home/user/waf/waf_pb2.py"
    pb2_grpc_file = "/home/user/waf/waf_pb2_grpc.py"

    assert os.path.isfile(pb2_file), f"Protobuf generated file {pb2_file} not found."
    assert os.path.isfile(pb2_grpc_file), f"gRPC generated file {pb2_grpc_file} not found."

def test_server_py_fixed():
    server_file = "/home/user/waf/server.py"
    assert os.path.isfile(server_file), f"File {server_file} is missing."

    with open(server_file, "r") as f:
        content = f.read()

    # Check that Python 2 print is removed or replaced with Python 3 print
    assert 'print "Server started"' not in content, "The Python 2 print statement is still in server.py."
    assert re.search(r'print\s*\(\s*(["\'])Server started\1\s*\)', content), "Could not find a valid Python 3 print('Server started') in server.py."

    # Check that the string is encoded before passing to C library
    assert ".encode(" in content or "bytes(" in content, "Did not find string encoding (.encode or bytes()) before passing to the C library in server.py."
    assert "lib.check_payload(request.payload)" not in content, "The buggy lib.check_payload(request.payload) is still in server.py. It must be encoded to bytes."

def test_migration_result():
    result_file = "/home/user/waf/migration_result.txt"
    assert os.path.isfile(result_file), f"The output file {result_file} was not created."

    with open(result_file, "r") as f:
        content = f.read().strip()

    expected = "Clean: False, Malicious: True"
    assert expected in content, f"Expected '{expected}' in {result_file}, but got:\n{content}"
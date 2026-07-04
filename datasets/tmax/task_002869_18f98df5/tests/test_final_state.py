# test_final_state.py

import os
import json
import pytest

def test_protobuf_files_generated():
    pb2_path = '/home/user/polyglot_service/math_ops_pb2.py'
    grpc_path = '/home/user/polyglot_service/math_ops_pb2_grpc.py'

    assert os.path.isfile(pb2_path), f"Expected protobuf generated file is missing: {pb2_path}"
    assert os.path.isfile(grpc_path), f"Expected gRPC generated file is missing: {grpc_path}"

def test_shared_library_compiled():
    so_path = '/home/user/polyglot_service/libmath.so'
    assert os.path.isfile(so_path), f"Shared library is missing: {so_path}"

def test_memory_leak_fixed():
    c_path = '/home/user/polyglot_service/libmath.c'
    assert os.path.isfile(c_path), f"C source file is missing: {c_path}"

    with open(c_path, 'r') as f:
        content = f.read()

    assert 'free(' in content, "The memory leak in libmath.c does not appear to be fixed (missing 'free(' statement)."

def test_result_json():
    result_path = '/home/user/result.json'
    assert os.path.isfile(result_path), f"Result file is missing: {result_path}"

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON.")

    assert "x" in data, "Result JSON missing 'x' key."
    assert "y" in data, "Result JSON missing 'y' key."
    assert "result" in data, "Result JSON missing 'result' key."

    assert data["x"] == 72, f"Expected x=72, got {data['x']}."
    assert data["y"] == 48, f"Expected y=48, got {data['y']}."
    assert data["result"] == 3456, f"Expected result=3456, got {data['result']}."
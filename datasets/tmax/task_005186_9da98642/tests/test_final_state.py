# test_final_state.py

import os
import pytest

def test_deploy_log_exists_and_correct():
    log_path = "/home/user/deploy_log.txt"
    assert os.path.exists(log_path), f"File {log_path} does not exist. The deployment check was not completed successfully."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "SUCCESS: 10.0", f"Expected 'SUCCESS: 10.0' in {log_path}, but got '{content}'"

def test_libprocessor_so_exists():
    so_path = "/home/user/release/libprocessor.so"
    assert os.path.exists(so_path), f"File {so_path} does not exist. The C library was not compiled."

def test_grpc_stubs_exist():
    pb2_path = "/home/user/release/data_pb2.py"
    pb2_grpc_path = "/home/user/release/data_pb2_grpc.py"
    assert os.path.exists(pb2_path), f"File {pb2_path} does not exist. gRPC stubs were not generated."
    assert os.path.exists(pb2_grpc_path), f"File {pb2_grpc_path} does not exist. gRPC stubs were not generated."

def test_grpc_server_abi_fixed():
    server_path = "/home/user/release/grpc_server.py"
    assert os.path.exists(server_path), f"File {server_path} is missing."

    with open(server_path, "r") as f:
        content = f.read()

    assert "ctypes.c_double" in content, "The ABI mismatch in grpc_server.py does not appear to be fixed to use ctypes.c_double."
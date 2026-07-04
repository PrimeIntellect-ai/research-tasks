# test_final_state.py

import os
import pytest

def test_output_log_content():
    log_path = "/home/user/project/output.log"
    assert os.path.isfile(log_path), f"Output log file {log_path} is missing."

    # Compute expected hex string dynamically
    input_bytes = b"SYSTEMS_PROGRAMMING"
    expected_bytes = bytes((b + 5) & 0xFF for b in input_bytes)
    expected_hex = expected_bytes.hex()

    with open(log_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content.lower() == expected_hex.lower(), (
        f"Content of {log_path} is incorrect. "
        f"Expected '{expected_hex}', but got '{actual_content}'."
    )

def test_rust_library_compiled():
    # Check that the release version of the shared library exists
    so_path = "/home/user/project/rust_lib/target/release/libprocessor.so"
    assert os.path.isfile(so_path), f"Compiled Rust library {so_path} is missing."

def test_grpc_bindings_generated():
    pb2_path = "/home/user/project/compute_pb2.py"
    pb2_grpc_path = "/home/user/project/compute_pb2_grpc.py"

    assert os.path.isfile(pb2_path), f"Generated protobuf file {pb2_path} is missing."
    assert os.path.isfile(pb2_grpc_path), f"Generated gRPC file {pb2_grpc_path} is missing."

def test_python_scripts_exist():
    server_path = "/home/user/project/server.py"
    client_path = "/home/user/project/client.py"

    assert os.path.isfile(server_path), f"Server script {server_path} is missing."
    assert os.path.isfile(client_path), f"Client script {client_path} is missing."
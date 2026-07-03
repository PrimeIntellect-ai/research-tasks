# test_final_state.py
import os
import subprocess
import pytest

def test_proto_file_exists():
    proto_path = "/home/user/shim.proto"
    assert os.path.isfile(proto_path), f"File {proto_path} is missing."

    with open(proto_path, 'r') as f:
        content = f.read()

    assert "package pipeline;" in content, "Proto file does not define package 'pipeline'."
    assert "service ShimBuilder" in content, "Proto file does not define service 'ShimBuilder'."
    assert "ShimRequest" in content, "Proto file does not define message 'ShimRequest'."
    assert "ShimResponse" in content, "Proto file does not define message 'ShimResponse'."

def test_proto_generated_files_exist():
    pb2_path = "/home/user/shim_pb2.py"
    pb2_grpc_path = "/home/user/shim_pb2_grpc.py"

    assert os.path.isfile(pb2_path), f"Generated file {pb2_path} is missing."
    assert os.path.isfile(pb2_grpc_path), f"Generated file {pb2_grpc_path} is missing."

def test_server_and_client_exist():
    assert os.path.isfile("/home/user/server.py"), "server.py is missing."
    assert os.path.isfile("/home/user/client.py"), "client.py is missing."

def test_output_bin_exists_and_executable():
    bin_path = "/home/user/output_bin"
    assert os.path.isfile(bin_path), f"Output binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Output binary {bin_path} is not executable."

def test_output_bin_execution():
    bin_path = "/home/user/output_bin"
    assert os.path.isfile(bin_path), f"Output binary {bin_path} is missing."

    # Run the binary and capture the exit code
    result = subprocess.run([bin_path], capture_output=True)
    assert result.returncode == 105, f"Expected exit code 105, got {result.returncode}."
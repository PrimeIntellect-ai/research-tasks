# test_final_state.py

import os
import pytest

def test_project_structure():
    dirs = [
        "/home/user/project",
        "/home/user/project/lib",
        "/home/user/project/grpc_gen",
        "/home/user/project/src",
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_shared_library_exists():
    so_path = "/home/user/project/lib/libcalc.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} does not exist."

def test_grpc_generated_files():
    pb2_path = "/home/user/project/grpc_gen/service_pb2.py"
    pb2_grpc_path = "/home/user/project/grpc_gen/service_pb2_grpc.py"
    assert os.path.isfile(pb2_path), f"Generated file {pb2_path} does not exist."
    assert os.path.isfile(pb2_grpc_path), f"Generated file {pb2_grpc_path} does not exist."

def test_source_files_exist():
    server_path = "/home/user/project/src/server.py"
    client_path = "/home/user/project/src/client.py"
    run_path = "/home/user/project/run.sh"
    assert os.path.isfile(server_path), f"Source file {server_path} does not exist."
    assert os.path.isfile(client_path), f"Source file {client_path} does not exist."
    assert os.path.isfile(run_path), f"Script {run_path} does not exist."

def test_output_file_content():
    output_path = "/home/user/project/output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == "46.5", f"Expected output.txt to contain '46.5', but got '{content}'."
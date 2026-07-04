# test_final_state.py

import os
import stat
import socket
import pytest

PROJECT_DIR = "/home/user/project"

def test_start_sh_exists_and_executable():
    script_path = os.path.join(PROJECT_DIR, "start.sh")
    assert os.path.isfile(script_path), f"Deployment script {script_path} does not exist."

    st = os.stat(script_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Deployment script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()
    assert "make all" in content, f"{script_path} does not seem to run 'make all'."

def test_server_pid_exists_and_valid():
    pid_file = os.path.join(PROJECT_DIR, "server.pid")
    assert os.path.isfile(pid_file), f"PID file {pid_file} was not created."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID. Found: '{pid_str}'"

    pid = int(pid_str)
    # Check if process is actually running (in Unix, sending signal 0 checks for existence)
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from {pid_file} is not running.")

def test_build_artifacts_exist():
    so_path = os.path.join(PROJECT_DIR, "build/libprocessor.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built."

    pb2_path = os.path.join(PROJECT_DIR, "python/metadata_pb2.py")
    assert os.path.isfile(pb2_path), f"Protobuf python file {pb2_path} was not generated."

    grpc_path = os.path.join(PROJECT_DIR, "python/metadata_pb2_grpc.py")
    assert os.path.isfile(grpc_path), f"gRPC python file {grpc_path} was not generated."

def test_cpp_bug_fixed():
    cpp_path = os.path.join(PROJECT_DIR, "cpp/processor.cpp")
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."

    with open(cpp_path, "r") as f:
        content = f.read()

    # The original buggy code used a 50-byte buffer and unsafe strcpy
    assert "char temp[50];" not in content, f"The 50-byte buffer overflow vulnerability is still present in {cpp_path}."
    assert "strcpy(" not in content, f"Unsafe 'strcpy' is still being used in {cpp_path}."

def test_makefile_completed():
    makefile_path = os.path.join(PROJECT_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "Not implemented" not in content, f"Makefile at {makefile_path} still contains the 'Not implemented' stub."
    assert "libprocessor.so" in content, f"Makefile at {makefile_path} does not contain rules for building libprocessor.so."
    assert "protoc" in content or "python -m grpc_tools.protoc" in content, f"Makefile at {makefile_path} does not contain rules for compiling protobufs."

def test_python_server_implemented():
    server_path = os.path.join(PROJECT_DIR, "python/server.py")
    assert os.path.isfile(server_path), f"Python server file {server_path} is missing."

    with open(server_path, "r") as f:
        content = f.read()

    assert "RESOURCE_EXHAUSTED" in content, f"Python server {server_path} does not seem to handle the RESOURCE_EXHAUSTED gRPC status code for rate limiting."
    assert "Rate limit exceeded" in content, f"Python server {server_path} does not contain the exact required error message 'Rate limit exceeded'."
    assert "ctypes" in content, f"Python server {server_path} does not seem to use ctypes to load the shared library."

def test_server_port_open():
    # Verify that a service is actually listening on port 50051
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        result = s.connect_ex(('127.0.0.1', 50051))
        assert result == 0, "The gRPC server does not appear to be listening on port 50051."
    finally:
        s.close()
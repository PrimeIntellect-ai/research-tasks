# test_final_state.py

import os
import stat
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/fix_and_test.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_c_file_patched():
    c_file_path = "/home/user/ws_grpc_proxy/c_ext/validator.c"
    assert os.path.isfile(c_file_path), f"C file {c_file_path} is missing."

    with open(c_file_path, "r") as f:
        content = f.read()

    assert "strncpy" in content, "The C file was not patched to use strncpy."
    assert "strcpy" not in content, "The unsafe strcpy call is still in the C file."

def test_proto_file_patched():
    proto_file_path = "/home/user/ws_grpc_proxy/proto/service.proto"
    assert os.path.isfile(proto_file_path), f"Protobuf file {proto_file_path} is missing."

    with open(proto_file_path, "r") as f:
        content = f.read()

    assert 'syntax = "proto3";' in content, "The Protobuf file was not patched to use proto3."
    assert 'proto2' not in content, "The proto2 syntax is still in the Protobuf file."

def test_project_built():
    binary_path = "/home/user/ws_grpc_proxy/target/debug/ws_grpc_proxy"
    assert os.path.isfile(binary_path), f"The project binary {binary_path} was not built. Did 'cargo build' run successfully?"

def test_ws_test_log():
    log_path = "/home/user/ws_test.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did the script run curl and save the output?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "HTTP/1.1 101 Switching Protocols" in content, "The ws_test.log does not contain the expected WebSocket upgrade response."
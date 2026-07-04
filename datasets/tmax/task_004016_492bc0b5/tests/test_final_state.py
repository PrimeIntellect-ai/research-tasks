# test_final_state.py
import os
import pytest

def test_system_proto_exists_and_valid():
    proto_path = "/home/user/system.proto"
    assert os.path.isfile(proto_path), f"File {proto_path} does not exist."
    with open(proto_path, "r") as f:
        content = f.read()
    assert "syntax" in content and "proto3" in content, "system.proto must use proto3 syntax."
    assert "service System" in content, "system.proto must define 'service System'."
    assert "rpc GetStatus" in content, "system.proto must define 'rpc GetStatus'."

def test_nginx_conf_configured_for_grpc():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "daemon off" in content, "nginx.conf must run in the foreground (daemon off)."
    assert "8080" in content, "nginx.conf must listen on port 8080."
    assert "http2" in content, "nginx.conf must use HTTP/2 for gRPC."
    assert "grpc_pass" in content and "127.0.0.1:50051" in content, "nginx.conf must forward gRPC traffic to 127.0.0.1:50051."

def test_update_patch_exists():
    patch_path = "/home/user/update.patch"
    assert os.path.isfile(patch_path), f"Patch file {patch_path} does not exist."

def test_check_system_script_patched():
    script_path = "/home/user/check_system.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    with open(script_path, "r") as f:
        content = f.read()
    assert "grpcurl" in content, "check_system.sh must use grpcurl."
    assert "-proto /home/user/system.proto" in content, "grpcurl must use the -proto flag with the proto file."
    assert "-plaintext" in content, "grpcurl must use the -plaintext flag."
    assert "8080" in content, "grpcurl must target the Nginx proxy on port 8080."

def test_success_log_contains_expected_output():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you redirect the output?"
    with open(log_path, "r") as f:
        content = f.read()
    assert "ALL_SYSTEMS_NOMINAL" in content, "success.log does not contain the expected gRPC response."
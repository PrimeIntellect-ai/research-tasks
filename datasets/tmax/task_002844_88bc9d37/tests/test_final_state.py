# test_final_state.py

import os
import re
import pytest

PROJECT_DIR = "/home/user/project"

def test_rust_extension_fixed():
    lib_rs_path = os.path.join(PROJECT_DIR, "rust_ext", "src", "lib.rs")
    assert os.path.isfile(lib_rs_path), f"File {lib_rs_path} is missing."

    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "-> String" in content, "The Rust extension was not fixed to return `String` instead of `&str`."
    assert "-> &str" not in content, "The Rust extension still returns `&str`, which causes a lifetime error."

def test_protobuf_schema_updated():
    proto_path = os.path.join(PROJECT_DIR, "proto", "service.proto")
    assert os.path.isfile(proto_path), f"File {proto_path} is missing."

    with open(proto_path, "r") as f:
        content = f.read()

    # Look for the multiplier field in ProcessRequest
    assert re.search(r"int32\s+multiplier\s*=\s*2\s*;", content), "The `multiplier` field was not added correctly to `service.proto`."

def test_grpc_files_generated():
    pb2_path = os.path.join(PROJECT_DIR, "service_pb2.py")
    pb2_grpc_path = os.path.join(PROJECT_DIR, "service_pb2_grpc.py")

    assert os.path.isfile(pb2_path), f"Generated gRPC file {pb2_path} is missing."
    assert os.path.isfile(pb2_grpc_path), f"Generated gRPC file {pb2_grpc_path} is missing."

def test_server_updated():
    server_path = os.path.join(PROJECT_DIR, "server.py")
    assert os.path.isfile(server_path), f"File {server_path} is missing."

    with open(server_path, "r") as f:
        content = f.read()

    assert "request.multiplier" in content, "The server does not appear to read `multiplier` from the request."
    # The multiplier should default to 1 if 0
    assert "1" in content and ("if" in content or "or" in content or "max" in content), "The server logic does not seem to handle the default multiplier correctly."

def test_test_server_created_and_valid():
    test_server_path = os.path.join(PROJECT_DIR, "test_server.py")
    assert os.path.isfile(test_server_path), f"Test file {test_server_path} is missing."

    with open(test_server_path, "r") as f:
        content = f.read()

    assert "@given" in content, "The property-based test does not use the `@given` decorator."
    assert "st.text" in content, "The property-based test does not generate random strings using `st.text`."
    assert "st.integers" in content, "The property-based test does not generate random integers using `st.integers`."
    assert "len(" in content, "The property-based test does not assert the length of the returned string."

def test_test_results_log():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Test results log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().lower()

    assert "passed" in content, "The test results log does not indicate that tests passed."
    assert "failed" not in content or "0 failed" in content, "The test results log indicates that some tests failed."
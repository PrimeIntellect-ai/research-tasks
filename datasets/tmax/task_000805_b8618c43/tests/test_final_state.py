# test_final_state.py

import os
import pytest

def test_qa_report_exists_and_correct():
    report_path = "/home/user/token-env/qa_report.txt"
    assert os.path.isfile(report_path), f"File not found: {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected = "VALIDATION_SUCCESS: 8a9d1c7e6b5f4a3d2c1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c"
    assert content == expected, f"Content of qa_report.txt is incorrect. Expected '{expected}', Got '{content}'"

def test_protobuf_generated():
    pb_go = "/home/user/token-env/auth/service.pb.go"
    grpc_go = "/home/user/token-env/auth/service_grpc.pb.go"

    assert os.path.isfile(pb_go), f"Protobuf Go file not generated: {pb_go}"
    assert os.path.isfile(grpc_go), f"gRPC Go file not generated: {grpc_go}"

def test_legacy_crypto_fixed():
    c_file = "/home/user/token-env/legacy_crypto.c"
    assert os.path.isfile(c_file), f"File not found: {c_file}"

    with open(c_file, "r") as f:
        content = f.read()

    assert "malloc(16)" not in content, "legacy_crypto.c still contains the buggy malloc(16)"

def test_makefile_fixed():
    makefile_path = "/home/user/token-env/Makefile"
    assert os.path.isfile(makefile_path), f"File not found: {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    # Check if standard shared library flags were added
    assert "-fPIC" in content or "-shared" in content, "Makefile does not seem to be fixed (missing -fPIC or -shared flags)"

def test_shared_library_exists():
    so_file = "/home/user/token-env/liblegacy_crypto.so"
    assert os.path.isfile(so_file), f"Shared library not successfully built: {so_file}"
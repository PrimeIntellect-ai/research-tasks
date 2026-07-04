# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/release_prep"

def test_libbilling_so_exists():
    filepath = os.path.join(BASE_DIR, "libbilling.so")
    assert os.path.isfile(filepath), f"Shared library {filepath} does not exist. Did you compile the C code?"

def test_billing_core_patched():
    filepath = os.path.join(BASE_DIR, "billing_core.c")
    assert os.path.isfile(filepath), f"File {filepath} is missing."
    with open(filepath, "r") as f:
        content = f.read()
    assert "current * 0.90" in content, f"The file {filepath} does not appear to be patched correctly."
    assert "current * 1.10" not in content, f"The file {filepath} still contains the bug."

def test_grpc_bindings_generated():
    pb2_file = os.path.join(BASE_DIR, "billing_pb2.py")
    pb2_grpc_file = os.path.join(BASE_DIR, "billing_pb2_grpc.py")

    assert os.path.isfile(pb2_file), f"gRPC binding file {pb2_file} is missing. Did you generate the bindings?"
    assert os.path.isfile(pb2_grpc_file), f"gRPC binding file {pb2_grpc_file} is missing. Did you generate the bindings?"

def test_server_py_exists():
    filepath = os.path.join(BASE_DIR, "server.py")
    assert os.path.isfile(filepath), f"Server script {filepath} does not exist."

def test_verify_release_py_exists():
    filepath = os.path.join(BASE_DIR, "verify_release.py")
    assert os.path.isfile(filepath), f"Verification script {filepath} does not exist."

def test_deployment_verification_log():
    filepath = os.path.join(BASE_DIR, "deployment_verification.log")
    assert os.path.isfile(filepath), f"Log file {filepath} does not exist. Did you run the verification script?"

    with open(filepath, "r") as f:
        content = f.read().strip()

    # Calculate the expected total based on the logic
    # Item 1: 100.0 (Odd) -> 100.0
    # Item 2: 200.0 (Even) -> 200.0 * 0.9 = 180.0
    # Item 3: 300.0 (Odd) -> 300.0
    expected_total = 100.0 + (200.0 * 0.90) + 300.0
    expected_string = f"FINAL_TOTAL: {expected_total}"

    assert expected_string in content, f"Log file {filepath} does not contain the expected text '{expected_string}'. Found: '{content}'"
# test_final_state.py

import sys
import os
import pytest

def fnv1a_hash(data: bytes) -> int:
    """Compute the FNV-1a hash exactly as the C extension does."""
    h = 14695981039346656037
    for b in data:
        h ^= b
        h *= 1099511628211
        h &= 0xFFFFFFFFFFFFFFFF
    return h

def test_c_extension_fixed():
    """Verify that the deliberate crash was removed from fasthash.c."""
    c_file = "/app/vendored/pyfasthash/fasthash.c"
    assert os.path.exists(c_file), f"{c_file} is missing."
    with open(c_file, "r") as f:
        content = f.read()
    assert '__asm__("ud2");' not in content, "fasthash.c still contains the deliberate crash instruction '__asm__(\"ud2\");'."

def test_setup_py_fixed():
    """Verify that the invalid compiler flag was removed from setup.py."""
    setup_file = "/app/vendored/pyfasthash/setup.py"
    assert os.path.exists(setup_file), f"{setup_file} is missing."
    with open(setup_file, "r") as f:
        content = f.read()
    assert "-Werror=invalid-flag-that-breaks-build" not in content, "setup.py still contains the invalid compiler flag."

def test_grpc_service():
    """Verify the gRPC service is running and correctly computes the hash."""
    sys.path.insert(0, "/home/user")
    try:
        import grpc
        import service_pb2
        import service_pb2_grpc
    except ImportError as e:
        pytest.fail(f"Failed to import grpc or the compiled protobuf files from /home/user: {e}")

    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = service_pb2_grpc.HashServiceStub(channel)

    # First test case
    test_items = ["hello", "world"]
    expected_string = "".join(test_items).encode('utf-8')
    expected_hash = fnv1a_hash(expected_string)

    request = service_pb2.HashRequest(items=test_items)
    try:
        response = stub.ComputeHash(request, timeout=3)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC ComputeHash call failed for {test_items}: {e}")

    assert response.hash_value == expected_hash, f"For items {test_items}, expected hash {expected_hash}, but got {response.hash_value}."

    # Second test case
    test_items2 = ["fast", "hash", "grpc", "test"]
    expected_string2 = "".join(test_items2).encode('utf-8')
    expected_hash2 = fnv1a_hash(expected_string2)
    request2 = service_pb2.HashRequest(items=test_items2)
    try:
        response2 = stub.ComputeHash(request2, timeout=3)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC ComputeHash call failed for {test_items2}: {e}")

    assert response2.hash_value == expected_hash2, f"For items {test_items2}, expected hash {expected_hash2}, but got {response2.hash_value}."
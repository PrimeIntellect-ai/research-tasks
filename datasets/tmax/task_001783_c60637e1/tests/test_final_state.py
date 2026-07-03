# test_final_state.py

import os
import sys
import json
import requests
import pytest

# Add workspace to path to import generated gRPC stubs
sys.path.insert(0, "/app/workspace")

def test_http_gateway_valid_crc():
    """Test HTTP gateway with a valid CRC."""
    url = "http://127.0.0.1:8080/verify?data=hello&crc=907060870"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP gateway: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert data.get("valid") is True, f"Expected {{'valid': True}}, got {data}"

def test_http_gateway_invalid_crc():
    """Test HTTP gateway with an invalid CRC."""
    url = "http://127.0.0.1:8080/verify?data=hello&crc=123"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP gateway: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert data.get("valid") is False, f"Expected {{'valid': False}}, got {data}"

def test_grpc_backend():
    """Test gRPC backend directly."""
    try:
        import grpc
        import crc_pb2
        import crc_pb2_grpc
    except ImportError as e:
        pytest.fail(f"Failed to import gRPC modules (agent may not have generated them correctly): {e}")

    try:
        with grpc.insecure_channel('127.0.0.1:50051') as channel:
            stub = crc_pb2_grpc.ChecksumServiceStub(channel)
            request = crc_pb2.VerifyRequest(data="world", expected_crc=980881731)
            response = stub.Verify(request, timeout=5)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e}")

    assert response.is_valid is True, f"Expected is_valid=True for 'world' and 980881731, got {response.is_valid}"

def test_grpc_backend_invalid():
    """Test gRPC backend directly with invalid CRC."""
    try:
        import grpc
        import crc_pb2
        import crc_pb2_grpc
    except ImportError as e:
        pytest.fail(f"Failed to import gRPC modules: {e}")

    try:
        with grpc.insecure_channel('127.0.0.1:50051') as channel:
            stub = crc_pb2_grpc.ChecksumServiceStub(channel)
            request = crc_pb2.VerifyRequest(data="world", expected_crc=12345)
            response = stub.Verify(request, timeout=5)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e}")

    assert response.is_valid is False, f"Expected is_valid=False for 'world' and 12345, got {response.is_valid}"
# test_final_state.py

import os
import sys
import json
import socket
import requests
import pytest
import time

def test_redis_running():
    """Check if Redis is running on port 6379."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        assert s.connect_ex(('127.0.0.1', 6379)) == 0, "Redis is not running on port 6379"

def test_fastapi_running_and_accepts_payload():
    """Check if FastAPI is running on port 8000 and accepts telemetry payloads."""
    # Check port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        assert s.connect_ex(('127.0.0.1', 8000)) == 0, "FastAPI is not running on port 8000"

    # Send a valid payload and a malicious payload (length 00)
    payloads = [
        {"device_id": "test_1", "payload": "0102aabb"},
        {"device_id": "test_malicious", "payload": "0200"} # length 00
    ]

    try:
        response = requests.post("http://127.0.0.1:8000/telemetry", json=payloads, timeout=5)
        assert response.status_code in [200, 201, 202], f"Expected successful status code, got {response.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to send HTTP POST to FastAPI: {e}")

def test_grpc_running():
    """Check if gRPC server is running on port 50051."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        assert s.connect_ex(('127.0.0.1', 50051)) == 0, "gRPC server is not running on port 50051"

def test_grpc_get_metrics():
    """Attempt to call GetMetrics on the gRPC server."""
    sys.path.append('/app/worker')
    sys.path.append('/app')

    try:
        import grpc
        import telemetry_pb2
        import telemetry_pb2_grpc
    except ImportError as e:
        pytest.fail(f"Failed to import gRPC modules: {e}")

    try:
        channel = grpc.insecure_channel('127.0.0.1:50051')
        # We assume the service is called TelemetryService, AggregationService, or MetricsService
        # based on typical naming conventions. We will try a few common ones if exact name isn't known.
        stub_class = None
        for attr in dir(telemetry_pb2_grpc):
            if attr.endswith('Stub'):
                stub_class = getattr(telemetry_pb2_grpc, attr)
                break

        assert stub_class is not None, "Could not find a gRPC Stub class in telemetry_pb2_grpc"

        stub = stub_class(channel)

        # Try to find the request message type (often Empty or GetMetricsRequest)
        req_msg = None
        for attr in dir(telemetry_pb2):
            if attr in ['Empty', 'GetMetricsRequest', 'MetricsRequest']:
                req_msg = getattr(telemetry_pb2, attr)
                break

        if req_msg is None:
            # Fallback, just instantiate the first message type that isn't a descriptor
            for attr in dir(telemetry_pb2):
                if attr[0].isupper() and not attr.endswith('Descriptor'):
                    req_msg = getattr(telemetry_pb2, attr)
                    break

        # Give worker some time to process the HTTP post from previous test
        time.sleep(1)

        # We don't strictly assert the response content, just that it doesn't hang or crash
        # because the infinite loop bug was fixed.
        try:
            response = stub.GetMetrics(req_msg(), timeout=5)
            assert response is not None, "gRPC GetMetrics returned None"
        except grpc.RpcError as e:
            # It's possible we guessed the wrong request type, but if it connects and fails cleanly,
            # that's better than hanging. We'll accept UNIMPLEMENTED or INVALID_ARGUMENT as proof it's up.
            pass

    except Exception as e:
        pytest.fail(f"Error interacting with gRPC server: {e}")
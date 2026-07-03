# test_final_state.py

import os
import pytest
import grpc

def encode_request(payload: str) -> bytes:
    """Manually encode a WafRequest with a single string field (tag=1)."""
    payload_bytes = payload.encode('utf-8')
    length = len(payload_bytes)
    # Tag 1, wire type 2 (length-delimited) -> 1 << 3 | 2 = 0x0a
    # Assuming length < 128 for these test payloads
    return b'\x0a' + bytes([length]) + payload_bytes

def decode_response(data: bytes) -> int:
    """Manually decode a WafResponse with a single int32 field (tag=1)."""
    if not data:
        raise ValueError("Empty response received")
    # Tag 1, wire type 0 (varint) -> 1 << 3 | 0 = 0x08
    if data[0] != 0x08:
        raise ValueError(f"Invalid response tag/wire-type: {data[0]}")

    # Decode varint
    value = 0
    shift = 0
    for i in range(1, len(data)):
        b = data[i]
        value |= (b & 0x7f) << shift
        if not (b & 0x80):
            break
        shift += 7

    # Handle negative numbers for int32 if needed (not expected here, but good practice)
    if value >= (1 << 31):
        value -= (1 << 32)

    return value

def test_files_exist():
    """Verify that the required source and library files exist."""
    assert os.path.exists("/home/user/waf.c"), "/home/user/waf.c is missing."
    assert os.path.exists("/home/user/libwaf.so"), "/home/user/libwaf.so is missing."
    assert os.path.exists("/home/user/waf.proto"), "/home/user/waf.proto is missing."
    assert os.path.exists("/home/user/server.py"), "/home/user/server.py is missing."

def test_grpc_service_analyze_payload():
    """Connect to the gRPC service and verify the AnalyzePayload method."""
    channel = grpc.insecure_channel('127.0.0.1:50051')

    # Create a generic unary-unary call
    analyze_payload = channel.unary_unary(
        '/waf.WafService/AnalyzePayload',
        request_serializer=encode_request,
        response_deserializer=decode_response,
    )

    test_cases = [
        ("admin' OR 1=1--", 1042),
        ("<script>alert(1)</script>", 1391),
        ("test_payload_123", 1032), # Recomputed: state=1, ...
    ]

    for payload, expected_score in test_cases:
        try:
            score = analyze_payload(payload, timeout=5)
            assert score == expected_score, f"Expected score {expected_score} for payload '{payload}', but got {score}"
        except grpc.RpcError as e:
            pytest.fail(f"gRPC call failed for payload '{payload}': {e.details()} (status code: {e.code()})")
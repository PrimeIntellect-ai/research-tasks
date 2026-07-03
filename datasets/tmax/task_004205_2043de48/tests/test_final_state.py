# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_router_verification_log():
    log_path = "/home/user/workspace/router_verification.log"
    clean_path = "/home/user/workspace/test_corpora/clean_routes.txt"
    evil_path = "/home/user/workspace/test_corpora/evil_routes.txt"

    assert os.path.isfile(log_path), f"Verification log missing at {log_path}"

    with open(clean_path, "r") as f:
        clean_lines = [line.strip() for line in f if line.strip()]
    with open(evil_path, "r") as f:
        evil_lines = [line.strip() for line in f if line.strip()]

    clean_count = len(clean_lines)
    evil_count = len(evil_lines)

    with open(log_path, "r") as f:
        log_content = f.read()

    assert f"CLEAN_PASSED: {clean_count}" in log_content, f"Log does not contain CLEAN_PASSED: {clean_count}. Content: {log_content}"
    assert f"EVIL_REJECTED: {evil_count}" in log_content, f"Log does not contain EVIL_REJECTED: {evil_count}. Content: {log_content}"

def test_grpc_server_transcription():
    proto_path = "/home/user/workspace/audio_router.proto"
    assert os.path.isfile(proto_path), f"Protobuf definition missing at {proto_path}"

    # We will try to test the gRPC server using a dynamically generated python client if grpcio-tools is available.
    # Otherwise, we will check if the server process is listening on port 50051.

    try:
        import grpc
        from grpc_tools import protoc
    except ImportError:
        # Fallback to checking if port 50051 is open and listening
        output = subprocess.check_output("ss -tuln | grep 50051", shell=True, text=True)
        assert "50051" in output, "gRPC server is not listening on port 50051"
        return

    # Compile the proto
    proto_dir = os.path.dirname(proto_path)
    sys.path.insert(0, proto_dir)

    protoc.main((
        '',
        f'-I{proto_dir}',
        f'--python_out={proto_dir}',
        f'--grpc_python_out={proto_dir}',
        proto_path,
    ))

    import audio_router_pb2
    import audio_router_pb2_grpc

    channel = grpc.insecure_channel('localhost:50051')
    stub = audio_router_pb2_grpc.AudioRouterStub(channel)

    request = audio_router_pb2.ProcessRequest(
        route_path="/v3/api/audio/transcribe/wav",
        audio_identifier="/app/audio_fixture.wav"
    )

    try:
        response = stub.ProcessRequest(request)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e}")

    assert response.accepted is True, "Expected request to be accepted"
    assert "Migration to C++ is complete" in response.result, f"Transcript missing or incorrect in result: {response.result}"
# test_final_state.py
import os
import sys
import subprocess
import pytest

def setup_proto():
    proto_content = """
    syntax = "proto3";
    package ci_video;

    service CIAnalyzer {
        rpc RunEmulator (RunRequest) returns (RunResponse);
    }

    message RunRequest {
        string video_path = 1;
    }

    message RunResponse {
        repeated int32 output = 1;
    }
    """
    proto_path = "/tmp/ci_analyzer_test.proto"
    with open(proto_path, "w") as f:
        f.write(proto_content)

    try:
        subprocess.check_call([
            sys.executable, "-m", "grpc_tools.protoc",
            "-I/tmp",
            "--python_out=/tmp",
            "--grpc_python_out=/tmp",
            proto_path
        ])
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile test protobuf: {e}")

    if "/tmp" not in sys.path:
        sys.path.insert(0, "/tmp")

@pytest.fixture(scope="module", autouse=True)
def prepare_grpc():
    setup_proto()
    try:
        import grpc
    except ImportError:
        pytest.fail("grpcio is not installed. The gRPC server cannot be tested.")

def test_grpc_unauthenticated():
    import grpc
    import ci_analyzer_test_pb2
    import ci_analyzer_test_pb2_grpc

    channel = grpc.insecure_channel('localhost:50051')
    stub = ci_analyzer_test_pb2_grpc.CIAnalyzerStub(channel)
    request = ci_analyzer_test_pb2.RunRequest(video_path="/app/ci_test_run.mp4")

    with pytest.raises(grpc.RpcError) as excinfo:
        stub.RunEmulator(request)

    assert excinfo.value.code() == grpc.StatusCode.UNAUTHENTICATED, \
        f"Expected UNAUTHENTICATED status code, got {excinfo.value.code()}"

def test_grpc_authenticated():
    import grpc
    import ci_analyzer_test_pb2
    import ci_analyzer_test_pb2_grpc

    channel = grpc.insecure_channel('localhost:50051')
    stub = ci_analyzer_test_pb2_grpc.CIAnalyzerStub(channel)
    request = ci_analyzer_test_pb2.RunRequest(video_path="/app/ci_test_run.mp4")
    metadata = (('authorization', 'Bearer secret-token-123'),)

    try:
        response = stub.RunEmulator(request, metadata=metadata)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e.details()} (Code: {e.code()})")

    actual_output = list(response.output)
    expected_output = [3, 4]
    assert actual_output == expected_output, \
        f"Expected emulator output {expected_output}, got {actual_output}"
# test_final_state.py

import os
import sys
import tempfile
import subprocess
import pytest

def test_executable_exists():
    path = "/home/user/audio_tool/analyzer"
    assert os.path.isfile(path), f"Compiled analyzer executable not found at {path}."
    assert os.access(path, os.X_OK), f"File at {path} is not executable."

def test_proto_exists():
    path = "/home/user/service/audio.proto"
    assert os.path.isfile(path), f"Protocol Buffers definition not found at {path}."

def test_server_exists():
    path = "/home/user/service/server.py"
    assert os.path.isfile(path), f"Python server implementation not found at {path}."

def test_grpc_service():
    proto_path = "/home/user/service/audio.proto"
    assert os.path.isfile(proto_path), "audio.proto must exist to test the service."

    try:
        import grpc
    except ImportError:
        pytest.fail("grpc module is not installed. It is required for the gRPC server.")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Compile the proto file dynamically to generate client stubs
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"-I{os.path.dirname(proto_path)}",
            f"--python_out={tmpdir}",
            f"--grpc_python_out={tmpdir}",
            proto_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to compile proto file using grpc_tools.protoc:\n{result.stderr}"

        sys.path.insert(0, tmpdir)
        try:
            import audio_pb2
            import audio_pb2_grpc

            channel = grpc.insecure_channel("localhost:50051")

            # Use reflection-like approach to find the correct Stub and Request classes
            # since the user might have named the request message anything.
            stub_class = getattr(audio_pb2_grpc, "AudioAnalysisStub", None)
            assert stub_class is not None, "AudioAnalysisStub not found in generated gRPC code."

            stub = stub_class(channel)

            service_desc = audio_pb2.DESCRIPTOR.services_by_name.get('AudioAnalysis')
            assert service_desc is not None, "Service 'AudioAnalysis' not found in audio.proto."

            method_desc = service_desc.methods_by_name.get('Analyze')
            assert method_desc is not None, "Method 'Analyze' not found in 'AudioAnalysis' service."

            req_class_name = method_desc.input_type.name
            req_class = getattr(audio_pb2, req_class_name)

            # Instantiate request and call the method
            req = req_class(file_path="/app/test_audio.wav")

            try:
                response = stub.Analyze(req, timeout=5)
            except grpc.RpcError as e:
                pytest.fail(f"gRPC call to Analyze failed: {e.details()} (status: {e.code()})")

            assert hasattr(response, "result_text"), "Response message does not have 'result_text' field."
            assert response.result_text == "EVENTS: 4", f"Expected response 'EVENTS: 4', got '{response.result_text}'"

        finally:
            sys.path.pop(0)
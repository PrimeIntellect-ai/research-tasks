# test_final_state.py

import os
import subprocess
import socket
import tempfile
import sys
import pytest

def test_grpc_server_listening():
    """Verify that the gRPC server is listening on 127.0.0.1:50051."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', 50051))
        assert result == 0, "gRPC server is not listening on 127.0.0.1:50051"
    finally:
        s.close()

def test_grpc_process_data():
    """Verify the ProcessData RPC returns the correct transformed data."""
    proto_path = "/home/user/broken_pr/service.proto"
    assert os.path.exists(proto_path), f"Proto file not found at {proto_path}"

    test_inputs = [
        b"hello world",
        b"\x00\xFF\x5A\xA5\x0F\xF0",
        b"Open-source maintainer test",
    ]

    # Create a temporary directory to generate the gRPC client code and run the test
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate the gRPC python code
        compile_cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"-I{os.path.dirname(proto_path)}",
            f"--python_out={tmpdir}",
            f"--grpc_python_out={tmpdir}",
            proto_path
        ]
        try:
            subprocess.run(compile_cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to compile proto file: {e.stderr.decode()}")

        # Write a client script to test the server
        client_script_path = os.path.join(tmpdir, "test_client.py")
        with open(client_script_path, "w") as f:
            f.write(f"""
import sys
import grpc
import service_pb2
import service_pb2_grpc

def run():
    channel = grpc.insecure_channel('127.0.0.1:50051')
    stub = service_pb2_grpc.FilterServiceStub(channel)

    # Read input from stdin
    input_data = sys.stdin.buffer.read()

    request = service_pb2.ProcessDataRequest(data=input_data)
    response = stub.ProcessData(request)

    sys.stdout.buffer.write(response.result)

if __name__ == '__main__':
    run()
""")

        for input_data in test_inputs:
            expected_output = bytes((~(b ^ 0x5A)) & 0xFF for b in input_data)

            try:
                env = os.environ.copy()
                env["PYTHONPATH"] = tmpdir
                result = subprocess.run(
                    [sys.executable, client_script_path],
                    input=input_data,
                    capture_output=True,
                    check=True,
                    env=env,
                    timeout=5
                )
                actual_output = result.stdout
                assert actual_output == expected_output, f"Expected {expected_output.hex()}, but got {actual_output.hex()} for input {input_data.hex()}"
            except subprocess.TimeoutExpired:
                pytest.fail("gRPC client request timed out")
            except subprocess.CalledProcessError as e:
                pytest.fail(f"gRPC client request failed: {e.stderr.decode()}")
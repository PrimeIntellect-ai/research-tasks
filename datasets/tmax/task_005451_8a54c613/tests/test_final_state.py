# test_final_state.py

import os
import sys
import tempfile
import subprocess
import pytest
import grpc

PROTO_CONTENT = """
syntax = "proto3";
package telemetry;

service TelemetryProcessor {
  rpc ProcessData (DataPacket) returns (ProcessResponse);
}

message DataPacket {
  bytes payload = 1;
}

message ProcessResponse {
  bool success = 1;
  bytes decoded_data = 2;
}
"""

@pytest.fixture(scope="module")
def grpc_stub():
    with tempfile.TemporaryDirectory() as tmpdir:
        proto_path = os.path.join(tmpdir, "telemetry.proto")
        with open(proto_path, "w") as f:
            f.write(PROTO_CONTENT)

        from grpc_tools import protoc
        protoc.main((
            '',
            f'-I{tmpdir}',
            f'--python_out={tmpdir}',
            f'--grpc_python_out={tmpdir}',
            proto_path,
        ))

        sys.path.insert(0, tmpdir)
        import telemetry_pb2
        import telemetry_pb2_grpc

        channel = grpc.insecure_channel('127.0.0.1:50051')
        stub = telemetry_pb2_grpc.TelemetryProcessorStub(channel)

        yield stub, telemetry_pb2

        sys.path.pop(0)

def get_encoded_payload(text: str) -> bytes:
    out = subprocess.check_output(["/app/legacy_encoder", text]).decode().strip()
    return bytes.fromhex(out)

def test_proto_file_exists():
    assert os.path.exists("/home/user/telemetry.proto"), "The protobuf file /home/user/telemetry.proto does not exist."

def test_server_valid_packet(grpc_stub):
    stub, pb2 = grpc_stub
    text = "hello_world"
    payload = get_encoded_payload(text)

    req = pb2.DataPacket(payload=payload)
    try:
        resp = stub.ProcessData(req, timeout=5)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e}")

    assert resp.success is True, "Expected success=True for valid packet"
    assert resp.decoded_data == text.encode(), "Decoded data does not match original text"

def test_server_single_bit_error(grpc_stub):
    stub, pb2 = grpc_stub
    text = "single_bit_test"
    payload = bytearray(get_encoded_payload(text))

    # Introduce a 1-bit error in the first byte
    payload[0] ^= 0x01

    req = pb2.DataPacket(payload=bytes(payload))
    try:
        resp = stub.ProcessData(req, timeout=5)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e}")

    assert resp.success is True, "Expected success=True for packet with 1-bit error (should be corrected)"
    assert resp.decoded_data == text.encode(), "Decoded data does not match original text after 1-bit correction"

def test_server_two_bit_error(grpc_stub):
    stub, pb2 = grpc_stub
    text = "two_bit_test"
    payload = bytearray(get_encoded_payload(text))

    # Introduce a 2-bit error in the first byte
    payload[0] ^= 0x03

    req = pb2.DataPacket(payload=bytes(payload))
    try:
        resp = stub.ProcessData(req, timeout=5)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e}")

    assert resp.success is False, "Expected success=False for packet with 2-bit error (uncorrectable)"
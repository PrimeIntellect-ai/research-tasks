# test_final_state.py

import os
import sys
import random
import subprocess
import pytest

def reference_crc(data: bytes, init_val: int) -> int:
    hash_val = init_val
    for b in data:
        hash_val ^= b
        hash_val = (hash_val * 0x811C9DC5) & 0xFFFFFFFF
    return hash_val

def test_grpc_service_accuracy():
    proto_path = "/home/user/crc_service/proto/crc.proto"
    assert os.path.isfile(proto_path), f"Proto file not found at {proto_path}"

    # Compile the proto file
    compile_cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"-I/home/user/crc_service/proto",
        "--python_out=/tmp",
        "--grpc_python_out=/tmp",
        proto_path
    ]

    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to compile proto file: {e.stderr}")

    sys.path.insert(0, "/tmp")

    try:
        import crc_pb2
        import crc_pb2_grpc
        import grpc
    except ImportError as e:
        pytest.fail(f"Failed to import generated grpc modules or grpc library: {e}")

    channel = grpc.insecure_channel('127.0.0.1:8080')
    try:
        stub = crc_pb2_grpc.CrcServiceStub(channel)
    except AttributeError:
        pytest.fail("CrcServiceStub not found in generated crc_pb2_grpc. Ensure the service is named 'CrcService'.")

    correct = 0
    total = 100

    try:
        for _ in range(total):
            data_len = random.randint(10, 1000)
            data = bytes([random.randint(0, 255) for _ in range(data_len)])
            init_val = random.randint(0, 0xFFFFFFFF)

            try:
                req = crc_pb2.CrcRequest(data=data, initial_value=init_val)
            except AttributeError:
                pytest.fail("CrcRequest not found or fields are incorrect. Ensure 'bytes data' and 'uint32 initial_value'.")

            resp = stub.ComputeCrc(req)

            expected = reference_crc(data, init_val)
            if getattr(resp, "checksum", None) == expected:
                correct += 1
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during gRPC call: {e}")

    accuracy = correct / total
    assert accuracy >= 1.0, f"Metric accuracy: {accuracy} is below threshold 1.0. Correct: {correct}/{total}"

def test_nginx_config_exists():
    nginx_conf = "/home/user/proxy/nginx.conf"
    assert os.path.isfile(nginx_conf), f"Nginx configuration not found at {nginx_conf}"
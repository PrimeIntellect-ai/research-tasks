# test_final_state.py

import os
import sys
import pytest

def test_ci_report():
    report_path = "/home/user/ci_report.txt"
    assert os.path.isfile(report_path), f"Log file {report_path} does not exist."
    with open(report_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 1, f"Expected exactly 1 line in ci_report.txt, got {len(content)}"
    assert "secure_service.proto" in content[0], "ci_report.txt does not contain 'secure_service.proto'."
    assert "vulnerable_service.proto" not in content[0], "ci_report.txt should not contain 'vulnerable_service.proto'."

def test_vulnerable_service_deleted():
    path = "/home/user/project/proto/vulnerable_service.proto"
    assert not os.path.exists(path), f"Vulnerable service file {path} should have been deleted."

def test_secure_service_exists():
    path = "/home/user/project/proto/secure_service.proto"
    assert os.path.isfile(path), f"Secure service file {path} should exist."

def test_compiled_protobufs_exist():
    pb2_path = "/home/user/project/src/secure_service_pb2.py"
    pb2_grpc_path = "/home/user/project/src/secure_service_pb2_grpc.py"
    assert os.path.isfile(pb2_path), f"Compiled protobuf file {pb2_path} does not exist."
    assert os.path.isfile(pb2_grpc_path), f"Compiled protobuf file {pb2_grpc_path} does not exist."

def test_server_pid_running():
    pid_path = "/home/user/server.pid"
    assert os.path.isfile(pid_path), f"PID file {pid_path} does not exist."
    with open(pid_path, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_path} does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

def test_grpc_server_logic():
    try:
        import grpc
    except ImportError:
        pytest.fail("grpcio library is not installed.")

    sys.path.insert(0, '/home/user/project/src')
    try:
        import secure_service_pb2
        import secure_service_pb2_grpc
    except ImportError as e:
        pytest.fail(f"Failed to import generated protobuf modules: {e}")

    try:
        channel = grpc.insecure_channel('localhost:50051')
        stub = secure_service_pb2_grpc.AuthServiceStub(channel)

        # Test valid token
        req = secure_service_pb2.TokenRequest(token="SECURE-1234567890")
        resp = stub.VerifyToken(req)
        assert resp.valid is True, "Token 'SECURE-1234567890' should be valid."

        # Test short token
        req = secure_service_pb2.TokenRequest(token="SECURE-SHORT")
        resp = stub.VerifyToken(req)
        assert resp.valid is False, "Token 'SECURE-SHORT' should be invalid (too short)."

        # Test token with DROP
        req = secure_service_pb2.TokenRequest(token="SECURE-12345DROP")
        resp = stub.VerifyToken(req)
        assert resp.valid is False, "Token 'SECURE-12345DROP' should be invalid (contains DROP)."

        # Test invalid prefix
        req = secure_service_pb2.TokenRequest(token="INVALID-1234567890")
        resp = stub.VerifyToken(req)
        assert resp.valid is False, "Token 'INVALID-1234567890' should be invalid (wrong prefix)."

    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed: {e}")
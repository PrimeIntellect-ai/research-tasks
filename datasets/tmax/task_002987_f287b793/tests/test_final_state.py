# test_final_state.py

import os
import subprocess
import time
import sys
import hmac
import hashlib
from concurrent import futures

def test_files_exist():
    assert os.path.isfile("/home/user/server.py"), "/home/user/server.py is missing"
    assert os.path.isfile("/home/user/test_auth.py"), "/home/user/test_auth.py is missing"

def test_user_pytest_passes():
    # Run the user's test suite
    # We must ensure the legacy binary is running since their test connects to it
    legacy_proc = subprocess.Popen(["/app/legacy_auth"])
    server_proc = subprocess.Popen(["python3", "/home/user/server.py"])
    time.sleep(2)

    try:
        result = subprocess.run(["pytest", "/home/user/test_auth.py"], capture_output=True, text=True)
        assert result.returncode == 0, f"User's test_auth.py failed:\n{result.stdout}\n{result.stderr}"
    finally:
        legacy_proc.terminate()
        server_proc.terminate()
        legacy_proc.wait()
        server_proc.wait()

def test_server_logic():
    import grpc
    import tempfile

    proto_path = "/home/user/rust_auth/proto/auth.proto"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Compile protobuf
        subprocess.run([
            sys.executable, "-m", "grpc_tools.protoc",
            f"-I{os.path.dirname(proto_path)}",
            f"--python_out={tmpdir}",
            f"--grpc_python_out={tmpdir}",
            proto_path
        ], check=True)

        sys.path.insert(0, tmpdir)
        import auth_pb2
        import auth_pb2_grpc

        server_proc = subprocess.Popen(["python3", "/home/user/server.py"])
        time.sleep(2)

        try:
            channel = grpc.insecure_channel('127.0.0.1:50051')
            stub = auth_pb2_grpc.AuthServiceStub(channel)

            test_cases = [
                ("admin", "login_attempt"),
                ("guest", "view_items")
            ]

            for user_id, payload in test_cases:
                req = auth_pb2.GenerateTokenRequest(user_id=user_id, payload=payload)
                resp = stub.GenerateToken(req, timeout=5)

                expected_token = hmac.new(
                    b"WINTERMUTE_2049", 
                    f"{user_id}|{payload}".encode(), 
                    hashlib.sha256
                ).hexdigest()

                assert resp.token == expected_token, f"Expected {expected_token}, got {resp.token}"
        finally:
            server_proc.terminate()
            server_proc.wait()
            sys.path.pop(0)
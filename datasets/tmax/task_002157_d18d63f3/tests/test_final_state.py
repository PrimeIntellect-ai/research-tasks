# test_final_state.py
import os
import sys
import tempfile
import subprocess
import importlib.util

def test_artifact_proto_exists():
    assert os.path.isfile("/app/artifact.proto"), "/app/artifact.proto does not exist"

def test_grpc_service_via_nginx():
    proto_path = "/app/artifact.proto"
    assert os.path.exists(proto_path), "Protobuf file missing."

    # Compile the protobuf dynamically
    with tempfile.TemporaryDirectory() as tmpdir:
        # We assume grpcio-tools is installed as the agent needed it
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"-I{os.path.dirname(proto_path)}",
            f"--python_out={tmpdir}",
            f"--grpc_python_out={tmpdir}",
            proto_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to compile protobuf:\n{result.stderr}"

        sys.path.insert(0, tmpdir)
        try:
            import grpc
            import artifact_pb2
            import artifact_pb2_grpc

            channel = grpc.insecure_channel('127.0.0.1:8080')
            stub = artifact_pb2_grpc.PatchServiceStub(channel)

            request = artifact_pb2.PatchRequest(
                original_content="Hello World\n",
                patch_content="--- a/file\n+++ b/file\n@@ -1 +1 @@\n-Hello World\n+Hello Universe\n"
            )

            try:
                response = stub.ApplyPatch(request, timeout=5)
            except grpc.RpcError as e:
                assert False, f"gRPC request failed: {e.details()} (status code: {e.code()})"

            assert response.patched_content == "Hello Universe\n", f"Expected 'Hello Universe\\n', got '{response.patched_content}'"
        finally:
            sys.path.pop(0)

def test_vendored_package_fixed():
    patcher_path = "/app/vendored/patch_manager/patcher.py"
    assert os.path.exists(patcher_path), f"{patcher_path} is missing"

    with open(patcher_path, "r") as f:
        content = f.read()

    assert "import diflib" not in content, "Bug 1 (diflib typo) is still present in patcher.py"
    assert 'return ""' not in content, "Bug 2 (hardcoded return) is still present in patcher.py"
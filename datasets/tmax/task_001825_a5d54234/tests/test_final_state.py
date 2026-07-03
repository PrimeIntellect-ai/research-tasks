# test_final_state.py

import os
import sys
import glob
import subprocess
import tempfile
import pytest

def test_grpc_server_running_and_validating():
    # Ensure corpora are generated
    workspace_dir = "/home/user/workspace"
    evil_dir = os.path.join(workspace_dir, "corpus", "evil")
    clean_dir = os.path.join(workspace_dir, "corpus", "clean")

    if not os.path.exists(evil_dir) or not os.path.exists(clean_dir):
        # Try to run make if corpora are not present
        subprocess.run(["make"], cwd=workspace_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    assert os.path.exists(evil_dir), f"Evil corpus directory not found at {evil_dir}"
    assert os.path.exists(clean_dir), f"Clean corpus directory not found at {clean_dir}"

    evil_files = glob.glob(os.path.join(evil_dir, "*.bin"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.bin"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    # Try importing grpc; the student must have installed it to complete the task
    try:
        import grpc
        from grpc_tools import protoc
    except ImportError:
        pytest.fail("grpcio or grpcio-tools is not installed. The gRPC server cannot be tested.")

    # Compile the protobuf dynamically to ensure we have the right interface
    proto_path = os.path.join(workspace_dir, "pipeline.proto")
    assert os.path.exists(proto_path), f"Protobuf definition not found at {proto_path}"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Compile proto
        protoc.main((
            '',
            f'-I{workspace_dir}',
            f'--python_out={tmpdir}',
            f'--grpc_python_out={tmpdir}',
            proto_path,
        ))

        sys.path.insert(0, tmpdir)
        try:
            import pipeline_pb2
            import pipeline_pb2_grpc
        except ImportError as e:
            pytest.fail(f"Failed to import compiled protobuf modules: {e}")

        # Connect to the gRPC server
        channel = grpc.insecure_channel('localhost:50051')
        try:
            grpc.channel_ready_future(channel).result(timeout=5)
        except grpc.FutureTimeoutError:
            pytest.fail("gRPC server is not listening on localhost:50051 or did not become ready in time.")

        stub = pipeline_pb2_grpc.AssetValidatorStub(channel)

        # Test evil corpus
        evil_bypassed = []
        for e_file in evil_files:
            with open(e_file, 'rb') as f:
                content = f.read()
            request = pipeline_pb2.AssetRequest(content=content)
            try:
                response = stub.ValidateAsset(request)
                if response.is_valid:
                    evil_bypassed.append(os.path.basename(e_file))
            except grpc.RpcError as e:
                pytest.fail(f"RPC failed on evil file {os.path.basename(e_file)}: {e}")

        # Test clean corpus
        clean_modified = []
        for c_file in clean_files:
            with open(c_file, 'rb') as f:
                content = f.read()
            request = pipeline_pb2.AssetRequest(content=content)
            try:
                response = stub.ValidateAsset(request)
                if not response.is_valid:
                    clean_modified.append(os.path.basename(c_file))
            except grpc.RpcError as e:
                pytest.fail(f"RPC failed on clean file {os.path.basename(c_file)}: {e}")

        # Summarize failures
        errors = []
        if evil_bypassed:
            errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
        if clean_modified:
            errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

        if errors:
            pytest.fail(" | ".join(errors))
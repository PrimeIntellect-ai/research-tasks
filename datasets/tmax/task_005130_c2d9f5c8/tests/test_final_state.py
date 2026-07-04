# test_final_state.py

import os
import sys
import pytest

def test_c_library_built():
    path = "/app/dep_resolver/libresolver.so"
    assert os.path.isfile(path), f"Expected shared library {path} to be built."

def test_proto_file_exists():
    path = "/app/proto/resolver.proto"
    assert os.path.isfile(path), f"Expected protobuf file {path} to exist."
    with open(path, 'r') as f:
        content = f.read()
        assert "syntax" in content and "proto3" in content, "Proto file should use proto3 syntax."
        assert "package ci;" in content, "Proto file should have package 'ci'."
        assert "service DependencyResolver" in content, "Proto file should define 'DependencyResolver' service."

def test_run_service_script():
    path = "/app/run_service.sh"
    assert os.path.isfile(path), f"Expected script {path} to exist."
    assert os.access(path, os.X_OK), f"Expected script {path} to be executable."

def test_grpc_service():
    sys.path.insert(0, '/app')
    try:
        import grpc
    except ImportError:
        pytest.fail("grpcio is not installed.")

    try:
        import resolver_pb2
        import resolver_pb2_grpc
    except ImportError as e:
        pytest.fail(f"Could not import generated protobuf modules from /app: {e}")

    channel = grpc.insecure_channel('127.0.0.1:50505')
    stub = resolver_pb2_grpc.DependencyResolverStub(channel)

    request = resolver_pb2.ResolveRequest(package_name="lib-core", current_version="1.2.0")
    metadata = (('authorization', 'Bearer S3cr3t_CI_882'),)

    try:
        response = stub.ResolveGraph(request, metadata=metadata, timeout=5)
    except grpc.RpcError as e:
        pytest.fail(f"gRPC call failed. Is the server running and accepting the auth token? Error: {e}")

    assert response.is_valid is True, "Expected is_valid to be True in the response."
    assert response.resolved_tree == "lib-core@1.2.0->deps@ok", f"Unexpected resolved_tree in the response: {response.resolved_tree}"
# test_final_state.py

import os
import pytest

def test_go_server_executable_exists():
    path = "/app/vendored/service-mesh/server/server"
    assert os.path.isfile(path), f"Go server executable not found at {path}. Did you build the Go code?"
    assert os.access(path, os.X_OK), f"Go server at {path} is not executable."

def test_protobuf_generated_files():
    pb2_path = "/app/vendored/service-mesh/client/service_pb2.py"
    pb2_grpc_path = "/app/vendored/service-mesh/client/service_pb2_grpc.py"
    assert os.path.isfile(pb2_path), f"Protobuf file {pb2_path} not found. Did you generate the protobufs?"
    assert os.path.isfile(pb2_grpc_path), f"Protobuf gRPC file {pb2_grpc_path} not found. Did you generate the protobufs?"

def test_property_based_test_exists():
    path = "/app/vendored/service-mesh/client/test_props.py"
    assert os.path.isfile(path), f"Property-based test file {path} not found."
    with open(path, "r") as f:
        content = f.read()
    assert "hypothesis" in content, "The property-based test does not appear to use the 'hypothesis' library."

def test_benchmark_throughput_metric():
    path = "/app/throughput.txt"
    assert os.path.isfile(path), f"Throughput output file {path} not found. Did you run the benchmark and save the output?"

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        rps = float(content)
    except ValueError:
        pytest.fail(f"Could not parse a float from {path}. Content was: {content}")

    assert rps >= 2000.0, f"RPS {rps} is less than the required threshold of 2000.0. Keep optimizing!"
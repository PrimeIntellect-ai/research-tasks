# test_final_state.py

import os
import glob
import json
import pytest

def test_extension_compiled():
    """Verify that the C-extension was successfully compiled."""
    so_files = glob.glob("/home/user/math_service/algo_ext*.so")
    assert len(so_files) > 0, "algo_ext shared object file (.so) is missing in /home/user/math_service/. Did you compile the extension?"

def test_proto_files_generated():
    """Verify that the gRPC stubs were generated."""
    pb2_path = "/home/user/math_service/service_pb2.py"
    pb2_grpc_path = "/home/user/math_service/service_pb2_grpc.py"

    assert os.path.isfile(pb2_path), f"{pb2_path} is missing. Did you generate the gRPC python files?"
    assert os.path.isfile(pb2_grpc_path), f"{pb2_grpc_path} is missing. Did you generate the gRPC python files?"

def test_benchmark_results():
    """Verify that the benchmark results JSON file exists and contains correct data."""
    json_path = "/home/user/math_service/benchmark_results.json"
    assert os.path.isfile(json_path), f"{json_path} is missing. Did you run the benchmark client?"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} contains invalid JSON.")

    assert "final_result" in data, "'final_result' key missing in benchmark_results.json"
    assert "total_time_seconds" in data, "'total_time_seconds' key missing in benchmark_results.json"

    final_result = data["final_result"]
    total_time = data["total_time_seconds"]

    assert isinstance(final_result, (int, float)), f"final_result must be a number, got {type(final_result).__name__}"
    assert isinstance(total_time, (int, float)), f"total_time_seconds must be a number, got {type(total_time).__name__}"

    # The expected result is approximately 0.693147 for n=100 and x=0.5
    assert 0.693 <= final_result <= 0.694, f"final_result {final_result} is out of expected range (0.693 to 0.694). Check your RPC call parameters."
    assert total_time > 0, f"total_time_seconds {total_time} must be greater than 0."
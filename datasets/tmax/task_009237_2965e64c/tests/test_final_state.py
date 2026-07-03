# test_final_state.py

import os
import json
import pytest

def test_report_json_exists_and_valid():
    report_path = '/home/user/math_perf/report.json'
    assert os.path.isfile(report_path), f"The file {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} is not valid JSON.")

    required_keys = ["rest_mean_latency_ms", "grpc_mean_latency_ms", "total_divisors_sum"]
    for key in required_keys:
        assert key in data, f"Key '{key}' is missing from {report_path}."

    assert isinstance(data["rest_mean_latency_ms"], (float, int)), "rest_mean_latency_ms must be a number."
    assert data["rest_mean_latency_ms"] > 0, "rest_mean_latency_ms must be greater than 0."

    assert isinstance(data["grpc_mean_latency_ms"], (float, int)), "grpc_mean_latency_ms must be a number."
    assert data["grpc_mean_latency_ms"] > 0, "grpc_mean_latency_ms must be greater than 0."

    assert isinstance(data["total_divisors_sum"], int), "total_divisors_sum must be an integer."
    assert data["total_divisors_sum"] == 4531853, f"total_divisors_sum is incorrect. Expected 4531853, got {data['total_divisors_sum']}."

def test_protobuf_compiled_files_exist():
    pb2_path = '/home/user/math_perf/math_service_pb2.py'
    pb2_grpc_path = '/home/user/math_perf/math_service_pb2_grpc.py'

    assert os.path.isfile(pb2_path), f"The compiled protobuf file {pb2_path} is missing."
    assert os.path.isfile(pb2_grpc_path), f"The compiled protobuf file {pb2_grpc_path} is missing."

def test_math_service_proto_contents():
    proto_path = '/home/user/math_perf/math_service.proto'
    assert os.path.isfile(proto_path), f"The file {proto_path} is missing."

    with open(proto_path, 'r') as f:
        content = f.read()

    assert "service MathService" in content, "MathService is not defined in math_service.proto."
    assert "message DivisorRequest" in content, "DivisorRequest is not defined in math_service.proto."
    assert "message DivisorResponse" in content, "DivisorResponse is not defined in math_service.proto."

def test_virtual_environment_exists():
    venv_path = '/home/user/venv'
    assert os.path.isdir(venv_path), f"The virtual environment directory {venv_path} is missing."

    python_bin = os.path.join(venv_path, 'bin', 'python')
    assert os.path.isfile(python_bin), f"Python executable missing in virtual environment at {python_bin}."
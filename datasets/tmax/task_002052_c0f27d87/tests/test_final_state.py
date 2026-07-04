# test_final_state.py

import os
import json
import pytest

def test_protobuf_compiled():
    pb2_path = "/home/user/math_service/math_service_pb2.py"
    pb2_grpc_path = "/home/user/math_service/math_service_pb2_grpc.py"

    assert os.path.isfile(pb2_path), f"Protobuf python file {pb2_path} is missing. Did you compile the proto file?"
    assert os.path.isfile(pb2_grpc_path), f"Protobuf grpc python file {pb2_grpc_path} is missing. Did you compile the proto file?"

def test_test_results_exists_and_valid():
    results_path = "/home/user/test_results.json"
    data_path = "/home/user/test_data.json"

    assert os.path.isfile(results_path), f"Results file {results_path} is missing. Did the E2E script generate it?"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Results file {results_path} is not valid JSON.")

    assert isinstance(results, list), "Results in test_results.json should be a JSON array."
    assert len(results) > 0, "Results array is empty."

    with open(data_path, 'r') as f:
        test_data = json.load(f)

    assert len(results) == len(test_data), f"Expected {len(test_data)} results, but found {len(results)}."

    # Check that all tests passed and match the expected schema
    for res in results:
        assert "expression" in res, "Result object is missing 'expression' key."
        assert "expected" in res, "Result object is missing 'expected' key."
        assert "actual" in res, "Result object is missing 'actual' key."
        assert "status" in res, "Result object is missing 'status' key."

        assert res["status"] == "PASS", (
            f"Test failed for expression: '{res.get('expression')}'. "
            f"Expected: {res.get('expected')}, Actual: {res.get('actual')}"
        )
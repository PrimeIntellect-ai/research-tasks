# test_final_state.py
import os
import pytest

def test_schema_proto_exists():
    proto_path = "/home/user/analytics_service/schema.proto"
    assert os.path.exists(proto_path), f"File {proto_path} is missing."

    with open(proto_path, "r") as f:
        content = f.read()
    assert "proto3" in content, "schema.proto must use proto3 syntax."
    assert "message DataBatch" in content, "schema.proto must define a DataBatch message."
    assert "repeated double" in content, "schema.proto must contain a repeated double field."

def test_executable_exists():
    exe_path = "/home/user/analytics_service/analytics_engine"
    assert os.path.exists(exe_path), f"Executable {exe_path} is missing. Did the Makefile run successfully?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_result_txt_content():
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"File {result_path} is missing. Did you run the analytics_engine and redirect output?"

    with open(result_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines of output in {result_path}, but found {len(lines)}."

    expected_mean = "Mean: 14.000000"
    expected_variance = "Variance: 7.700000"

    assert lines[0] == expected_mean, f"First line of {result_path} was '{lines[0]}', expected '{expected_mean}'."
    assert lines[1] == expected_variance, f"Second line of {result_path} was '{lines[1]}', expected '{expected_variance}'."
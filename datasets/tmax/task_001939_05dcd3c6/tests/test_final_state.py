# test_final_state.py

import os
import pytest

def test_build_artifacts_exist():
    pb2_path = "/home/user/math_dag/math_graph_pb2.py"
    grpc_pb2_path = "/home/user/math_dag/math_graph_pb2_grpc.py"

    assert os.path.isfile(pb2_path), f"Build artifact missing: {pb2_path}. Did you run make build?"
    assert os.path.isfile(grpc_pb2_path), f"Build artifact missing: {grpc_pb2_path}. Did you fix the Makefile and run make build?"

def test_makefile_fixed():
    makefile_path = "/home/user/math_dag/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} is missing"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "--grpc_python_out" in content, "Makefile does not seem to contain the fix for generating gRPC stubs."

def test_server_py_fixed():
    server_path = "/home/user/math_dag/server.py"
    assert os.path.isfile(server_path), f"{server_path} is missing"
    with open(server_path, "r") as f:
        content = f.read()
    assert "in_degree[curr] -= 1" not in content, "server.py still contains the bug 'in_degree[curr] -= 1'."

def test_output_matches_expected():
    output_path = "/home/user/math_dag/output.txt"
    expected_path = "/home/user/math_dag/expected.txt"

    assert os.path.isfile(output_path), f"{output_path} is missing. Did you run the client?"
    assert os.path.isfile(expected_path), f"{expected_path} is missing."

    with open(output_path, "r") as f:
        output_content = f.read().strip()

    with open(expected_path, "r") as f:
        expected_content = f.read().strip()

    assert output_content == expected_content, "The generated output.txt does not match expected.txt. The topological sort might still be incorrect."

def test_diff_result_empty():
    diff_path = "/home/user/math_dag/diff_result.txt"
    assert os.path.isfile(diff_path), f"{diff_path} is missing. Did you run the diff command and save the output?"

    with open(diff_path, "r") as f:
        diff_content = f.read().strip()

    assert diff_content == "", f"{diff_path} is not empty. There are differences between output.txt and expected.txt."
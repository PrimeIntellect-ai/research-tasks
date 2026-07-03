# test_final_state.py

import os
import re
import pytest

def test_graph_proto_fixed():
    proto_path = "/home/user/graph_service/graph.proto"
    assert os.path.isfile(proto_path), f"{proto_path} is missing"

    with open(proto_path, "r") as f:
        content = f.read()

    assert "repeated Edge edges" in content, "graph.proto does not contain the fixed 'repeated Edge edges = 1;' syntax"
    assert "repeated edges = 1;" not in content, "graph.proto still contains the syntax error"

def test_protobuf_compiled():
    pb2_path = "/home/user/graph_service/graph_pb2.py"
    pb2_grpc_path = "/home/user/graph_service/graph_pb2_grpc.py"

    assert os.path.isfile(pb2_path), f"Compiled protobuf file {pb2_path} is missing"
    assert os.path.isfile(pb2_grpc_path), f"Compiled gRPC stub file {pb2_grpc_path} is missing"

def test_e2e_script_exists():
    e2e_path = "/home/user/graph_service/test_e2e.py"
    assert os.path.isfile(e2e_path), f"End-to-end test script {e2e_path} is missing"

def test_result_txt_content():
    result_path = "/home/user/graph_service/result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} is missing"

    with open(result_path, "r") as f:
        content = f.read().strip()

    # Extract just the numbers to ignore formatting differences like spaces
    numbers = re.findall(r'\d+', content)
    expected_numbers = ['1', '2', '4', '3', '5', '6']

    assert numbers == expected_numbers, f"result.txt content is incorrect. Expected {expected_numbers}, got {numbers}"
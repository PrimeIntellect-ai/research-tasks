# test_final_state.py

import os
import pytest

def test_compiled_pb2_files_exist():
    pb2_path = "/home/user/repo/inventory_pb2.py"
    pb2_grpc_path = "/home/user/repo/inventory_pb2_grpc.py"

    assert os.path.isfile(pb2_path), f"Expected file {pb2_path} does not exist. Did you compile the proto file?"
    assert os.path.isfile(pb2_grpc_path), f"Expected file {pb2_grpc_path} does not exist. Did you compile the proto file with grpc stubs?"

def test_rpc_methods_txt_exists_and_correct():
    txt_path = "/home/user/rpc_methods.txt"
    assert os.path.isfile(txt_path), f"Expected file {txt_path} does not exist."

    with open(txt_path, 'r') as f:
        content = f.read().strip().splitlines()

    expected_methods = [
        "CreateItem",
        "DeleteItem",
        "GetItem",
        "ListItems",
        "UpdateItem"
    ]

    # Strip any potential trailing/leading whitespaces from each line
    actual_methods = [line.strip() for line in content if line.strip()]

    assert actual_methods == expected_methods, f"Contents of {txt_path} do not match the expected sorted method names. Expected {expected_methods}, got {actual_methods}."

def test_inventory_proto_is_fixed():
    proto_path = "/home/user/repo/inventory.proto"
    assert os.path.isfile(proto_path), f"File {proto_path} does not exist."

    with open(proto_path, 'r') as f:
        content = f.read()

    assert "rpc CreateItem" in content, "The CreateItem rpc is missing from the proto file. Was the patch applied?"
    assert "rpc UpdateItem" in content, "The UpdateItem rpc is missing from the proto file. Was the patch applied?"

    # Check that CreateItem has a semicolon
    lines = content.splitlines()
    create_item_line = next((line for line in lines if "rpc CreateItem" in line), None)
    assert create_item_line is not None, "Could not find 'rpc CreateItem' line."
    assert create_item_line.strip().endswith(";"), "The 'rpc CreateItem' line is missing the closing semicolon."
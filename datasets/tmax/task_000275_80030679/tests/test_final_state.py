# test_final_state.py
import os

def test_proto_file_exists():
    assert os.path.isfile('/home/user/workspace/migration.proto'), "migration.proto is missing"

def test_server_go_exists():
    assert os.path.isfile('/home/user/workspace/server.go'), "server.go is missing"

def test_proto_generated_files():
    # Check that protoc generated the Go files
    pb_go = '/home/user/workspace/migration/migration.pb.go'
    grpc_go = '/home/user/workspace/migration/migration_grpc.pb.go'
    assert os.path.isfile(pb_go) or os.path.isfile(grpc_go), "Generated protobuf Go files are missing in /home/user/workspace/migration/"

def test_patched_py_content():
    patched_file = '/home/user/workspace/patched.py'
    assert os.path.isfile(patched_file), f"{patched_file} is missing"

    expected_content = (
        "from setuptools import setup\n"
        "print('Installing package...')\n"
        "setup(\n"
        "    name='mypkg',\n"
        "    version='1.0',\n"
        ")"
    )

    with open(patched_file, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content.strip(), f"Content of {patched_file} does not match the expected patched output."
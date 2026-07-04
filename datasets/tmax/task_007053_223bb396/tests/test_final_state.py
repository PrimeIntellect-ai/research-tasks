# test_final_state.py
import os
import json
import sys

def test_proto_graph_json():
    graph_path = '/home/user/proto_graph.json'
    assert os.path.isfile(graph_path), f"File not found: {graph_path}"

    with open(graph_path, 'r') as f:
        try:
            graph = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{graph_path} is not valid JSON"

    expected_graph = {
        "base.proto": [],
        "user.proto": ["base.proto"],
        "service.proto": ["user.proto"]
    }

    assert graph == expected_graph, f"Graph content mismatch. Expected {expected_graph}, got {graph}"

def test_generated_directory():
    gen_dir = '/home/user/generated'
    assert os.path.isdir(gen_dir), f"Directory not found: {gen_dir}"

    expected_files = ['__init__.py', 'base_pb2.py', 'user_pb2.py', 'service_pb2.py']
    for f in expected_files:
        file_path = os.path.join(gen_dir, f)
        assert os.path.isfile(file_path), f"Expected generated file not found: {file_path}"

def test_test_serde_script_exists():
    script_path = '/home/user/test_serde.py'
    assert os.path.isfile(script_path), f"Script not found: {script_path}"

def test_payload_bin_content():
    payload_path = '/home/user/payload.bin'
    assert os.path.isfile(payload_path), f"Payload file not found: {payload_path}"

    gen_dir = '/home/user/generated'
    if gen_dir not in sys.path:
        sys.path.insert(0, gen_dir)

    try:
        import service_pb2
        import base_pb2
    except ImportError as e:
        assert False, f"Failed to import generated protobuf modules: {e}"

    with open(payload_path, 'rb') as f:
        data = f.read()

    msg = service_pb2.UserResponse()
    try:
        msg.ParseFromString(data)
    except Exception as e:
        assert False, f"Failed to parse payload.bin: {e}"

    assert msg.message == "Success", f"Expected message='Success', got {msg.message}"
    assert msg.user.id == 42, f"Expected user.id=42, got {msg.user.id}"
    assert msg.user.name == "Bob", f"Expected user.name='Bob', got {msg.user.name}"
    assert msg.user.status == base_pb2.OK, f"Expected user.status=OK, got {msg.user.status}"
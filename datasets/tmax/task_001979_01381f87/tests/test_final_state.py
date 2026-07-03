# test_final_state.py

import os

def test_project_structure():
    """Ensure the required directories and files exist."""
    base_dir = "/home/user/project"
    assert os.path.exists(base_dir), f"Directory {base_dir} is missing."

    # Check C library
    c_lib = os.path.join(base_dir, "c_src", "libtransform.so")
    assert os.path.exists(c_lib), f"C shared library {c_lib} is missing."

    # Check Protobuf
    proto_dir = os.path.join(base_dir, "proto")
    assert os.path.exists(proto_dir), f"Protobuf directory {proto_dir} is missing."
    assert any(f.endswith(".proto") for f in os.listdir(proto_dir)), "No .proto file found in proto directory."

    # Check Go server
    go_server = os.path.join(base_dir, "go_server", "server")
    assert os.path.exists(go_server), f"Go server binary {go_server} is missing."

    # Check Python proxy
    proxy_script = os.path.join(base_dir, "proxy", "proxy.py")
    assert os.path.exists(proxy_script), f"Python proxy script {proxy_script} is missing."

def test_result_bin_content():
    """Verify the result.bin file contains the correct XOR-transformed data."""
    result_file = "/home/user/project/result.bin"
    assert os.path.exists(result_file), f"Result file {result_file} is missing."

    with open(result_file, "rb") as f:
        actual_bytes = f.read()

    input_str = b"ORBITAL_DATA_STREAM_XYZ"
    expected_bytes = bytes(c ^ 0x42 for c in input_str)

    assert actual_bytes == expected_bytes, (
        f"Content of {result_file} is incorrect.\n"
        f"Expected hex: {expected_bytes.hex()}\n"
        f"Actual hex:   {actual_bytes.hex()}"
    )
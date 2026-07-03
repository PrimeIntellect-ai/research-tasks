# test_final_state.py

import os
import pytest

def test_missing_dep_txt():
    """Check that missing_dep.txt contains the correct missing dependency."""
    file_path = "/home/user/missing_dep.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."
    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == "common/v2/types.proto", f"Expected 'common/v2/types.proto' in {file_path}, but got '{content}'"

def test_patch_applied():
    """Check that the patch was applied successfully to token.proto."""
    token_proto_path = "/home/user/proto_deps/auth/v2/token.proto"
    assert os.path.isfile(token_proto_path), f"File {token_proto_path} does not exist."
    with open(token_proto_path, "r") as f:
        content = f.read()
    assert 'import "common/v1/types.proto";' in content, f"Expected patched import 'common/v1/types.proto' in {token_proto_path}."
    assert 'import "common/v2/types.proto";' not in content, f"Buggy import 'common/v2/types.proto' is still present in {token_proto_path}."

def test_gen_directory_contents():
    """Check that the generated python gRPC files exist in the gen directory."""
    gen_dir = "/home/user/gen"
    assert os.path.isdir(gen_dir), f"Directory {gen_dir} does not exist."

    expected_files = [
        "api/v1/gateway_pb2.py",
        "api/v1/gateway_pb2_grpc.py"
    ]

    for f in expected_files:
        file_path = os.path.join(gen_dir, f)
        assert os.path.isfile(file_path), f"Expected generated file {file_path} does not exist."

def test_script_exists():
    """Check that the test_gateway.py script exists."""
    script_path = "/home/user/test_gateway.py"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

def test_result_log():
    """Check that test_result.log contains exactly 'TEST_PASSED'."""
    log_path = "/home/user/test_result.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. The test script might not have run or failed."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "TEST_PASSED", f"Expected 'TEST_PASSED' in {log_path}, but got '{content}'"
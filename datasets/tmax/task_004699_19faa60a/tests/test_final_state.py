# test_final_state.py

import os
import pytest

def test_success_log_exists_and_content():
    """Check if success.log exists and contains the correct string."""
    log_path = "/home/user/pipeline/success.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "Successfully built service version 2.0.1"
    assert content == expected, f"Expected '{expected}' in {log_path}, got '{content}'"

def test_generated_go_files_exist():
    """Check if the generated Go files for the highest version exist."""
    pb_go = "/home/user/pipeline/api/service_2.0.1.pb.go"
    grpc_pb_go = "/home/user/pipeline/api/service_2.0.1_grpc.pb.go"

    assert os.path.isfile(pb_go), f"Generated file {pb_go} is missing."
    assert os.path.isfile(grpc_pb_go), f"Generated file {grpc_pb_go} is missing."

def test_other_versions_not_compiled():
    """Check that lower versions or pre-releases were not compiled."""
    api_dir = "/home/user/pipeline/api"
    if not os.path.isdir(api_dir):
        return  # handled by test_generated_go_files_exist

    files = os.listdir(api_dir)
    invalid_versions = ["1.5.9", "1.12.0", "2.0.1-rc.1"]

    for v in invalid_versions:
        pb_go = f"service_{v}.pb.go"
        grpc_pb_go = f"service_{v}_grpc.pb.go"

        assert pb_go not in files, f"File {pb_go} should not have been generated."
        assert grpc_pb_go not in files, f"File {grpc_pb_go} should not have been generated."
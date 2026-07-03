# test_final_state.py

import os
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_upgrade_pipeline():
    """
    Executes the student's pipeline script to perform the migration,
    since the task is to *write* the script that automates these steps.
    """
    script_path = "/home/user/upgrade_pipeline.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable. Did you run chmod +x?"

    # Run the script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, (
        f"The script {script_path} failed with return code {result.returncode}.\n"
        f"Stdout:\n{result.stdout}\n"
        f"Stderr:\n{result.stderr}"
    )

def test_modern_app_directory_created():
    assert os.path.isdir("/home/user/modern_app"), "The /home/user/modern_app directory was not created."

def test_schema_proto_upgraded_to_proto3():
    proto_path = "/home/user/modern_app/schema.proto"
    assert os.path.isfile(proto_path), f"The file {proto_path} is missing."

    with open(proto_path, "r") as f:
        content = f.read()

    assert 'syntax = "proto3";' in content, "schema.proto syntax declaration was not updated to 'proto3'."
    assert 'required ' not in content, "schema.proto still contains the 'required' field label, which is invalid in proto3."

def test_grpc_bindings_compiled():
    pb2_path = "/home/user/modern_app/schema_pb2.py"
    pb2_grpc_path = "/home/user/modern_app/schema_pb2_grpc.py"

    assert os.path.isfile(pb2_path), f"gRPC binding {pb2_path} was not generated."
    assert os.path.isfile(pb2_grpc_path), f"gRPC binding {pb2_grpc_path} was not generated."

def test_service_py_upgraded_to_python3():
    service_path = "/home/user/modern_app/service.py"
    assert os.path.isfile(service_path), f"The file {service_path} is missing."

    with open(service_path, "r") as f:
        content = f.read()

    assert 'import http.server as BaseHTTPServer' in content, "service.py did not update the BaseHTTPServer import."
    assert 'import urllib.parse as urlparse' in content, "service.py did not update the urlparse import."
    assert 'print(' in content, "service.py did not update print statements to Python 3 function calls."
    assert 'print "' not in content, "service.py still contains Python 2 print statements."

def test_migration_result_log_correct():
    log_path = "/home/user/migration_result.log"
    assert os.path.isfile(log_path), f"The file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "Processed: migrate_me"
    assert content == expected, f"Expected {log_path} to contain '{expected}', but got '{content}'."
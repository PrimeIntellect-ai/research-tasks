# test_final_state.py

import os
import json
import subprocess
import pytest

def test_version_check_script():
    """Check if version_check.py exists and exits with code 0 for the default config."""
    script_path = "/home/user/version_check.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # The default config.json has version 1.7.4, which should result in exit code 0
    result = subprocess.run(["python3", script_path], capture_output=True)
    assert result.returncode == 0, f"{script_path} did not exit with code 0. Stderr: {result.stderr.decode()}"

def test_proto_files_exist():
    """Check if the protobuf file and its compiled python outputs exist."""
    expected_files = [
        "/home/user/math_port/math_dag.proto",
        "/home/user/math_port/math_dag_pb2.py",
        "/home/user/math_port/math_dag_pb2_grpc.py"
    ]
    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Expected file {file_path} does not exist."

def test_server_and_client_scripts_exist():
    """Check if the server and client scripts exist."""
    expected_files = [
        "/home/user/math_port/server.py",
        "/home/user/math_port/client.py"
    ]
    for file_path in expected_files:
        assert os.path.isfile(file_path), f"Expected file {file_path} does not exist."

def test_result_json():
    """Check if result.json exists and contains the correctly evaluated graph values."""
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist. Did you run the client?"

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} does not contain valid JSON.")

    expected_data = {
        "A": 3.5,
        "B": 2.0,
        "C": 5.5,
        "D": 19.25,
        "E": 21.25
    }

    assert data == expected_data, f"Result JSON does not match expected evaluated values. Expected {expected_data}, got {data}."

    # Check if keys are sorted alphabetically in the file representation as requested
    with open(result_path, "r") as f:
        raw_content = f.read()

    # Find the positions of the keys in the raw JSON string to verify order
    pos_A = raw_content.find('"A"')
    pos_B = raw_content.find('"B"')
    pos_C = raw_content.find('"C"')
    pos_D = raw_content.find('"D"')
    pos_E = raw_content.find('"E"')

    assert pos_A < pos_B < pos_C < pos_D < pos_E, "Keys in result.json are not sorted alphabetically."
# test_final_state.py
import os
import json
import pytest

RESULT_FILE = "/home/user/test_result.json"
PROJECT_DIR = "/home/user/grpc_state_service"

def test_result_file_exists():
    assert os.path.isfile(RESULT_FILE), f"The result file {RESULT_FILE} was not generated. Did you run client_test.py?"

def test_result_file_contents():
    with open(RESULT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULT_FILE} is not a valid JSON file.")

    assert "status" in data, "Result JSON missing 'status' key."
    assert "final_state" in data, "Result JSON missing 'final_state' key."

    assert data["status"] == "success", f"Expected status 'success', got '{data['status']}'."
    assert data["final_state"] == "STOPPED", f"Expected final_state 'STOPPED', got '{data['final_state']}'."

def test_service_proto_fixed():
    proto_file = os.path.join(PROJECT_DIR, "service.proto")
    assert os.path.isfile(proto_file), f"{proto_file} is missing."

    with open(proto_file, "r") as f:
        content = f.read()

    assert "sequence_number" in content, "service.proto is missing the 'sequence_number' field in ParseRequest."
    assert "int32" in content, "service.proto should define 'sequence_number' as an int32."

def test_server_py_fixed():
    server_file = os.path.join(PROJECT_DIR, "server.py")
    assert os.path.isfile(server_file), f"{server_file} is missing."

    with open(server_file, "r") as f:
        content = f.read()

    assert '"HALT":' in content or "'HALT':" in content, "server.py still contains the state machine bug (missing 'HALT' transition)."
    assert '"HLT":' not in content and "'HLT':" not in content, "server.py should not contain the 'HLT' typo."
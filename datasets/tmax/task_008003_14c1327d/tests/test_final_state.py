# test_final_state.py
import os
import subprocess
import json
import pytest

def test_c_app_built_and_runs():
    app_path = "/home/user/artifact/src/app"
    assert os.path.isfile(app_path), f"Expected {app_path} to exist. Did you run 'make' after fixing the code?"
    assert os.access(app_path, os.X_OK), f"Expected {app_path} to be executable."

    result = subprocess.run([app_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Expected app to exit with code 0, but got {result.returncode}."
    assert "Artifact Built" in result.stdout, "Expected app output to contain 'Artifact Built'."

def test_http_response_log():
    log_path = "/home/user/http_response.log"
    assert os.path.isfile(log_path), f"Expected {log_path} to exist. Did you save the curl output?"
    with open(log_path, "r") as f:
        content = f.read()
    assert "job123" in content, "Expected http_response.log to contain 'job123' indicating the job was processed."

def test_grpc_response_log():
    log_path = "/home/user/grpc_response.log"
    assert os.path.isfile(log_path), f"Expected {log_path} to exist. Did you save the grpcurl output?"
    with open(log_path, "r") as f:
        content = f.read()

    try:
        data = json.loads(content)
        assert data.get("status") == "COMPLETED", "Expected gRPC JSON response to have status 'COMPLETED'."
    except json.JSONDecodeError:
        assert '"status"' in content and '"COMPLETED"' in content, "Expected gRPC response to contain 'COMPLETED' status."
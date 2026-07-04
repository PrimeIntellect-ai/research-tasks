# test_final_state.py
import os
import json
import pytest

def test_hardening_report_exists_and_valid():
    report_path = "/home/user/hardening_report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} was not created."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {report_path} is not valid JSON.")

    assert "container_name" in data, "Missing 'container_name' in report."
    assert data["container_name"] == "secure-con-01", f"Expected container_name 'secure-con-01', got '{data['container_name']}'."

    assert "storage_allocated" in data, "Missing 'storage_allocated' in report."
    # We allow both int and string representation of int, though the prompt says integer value
    assert int(data["storage_allocated"]) == 1024, f"Expected storage_allocated to be 1024, got {data['storage_allocated']}."

    assert "status" in data, "Missing 'status' in report."
    assert data["status"] == "stopped", f"Expected status 'stopped', got '{data['status']}'."

    assert "container_id" in data, "Missing 'container_id' in report."
    container_id = data["container_id"]
    assert isinstance(container_id, str) and len(container_id) > 0, "Invalid 'container_id' in report."

    pid_file = f"/home/user/run/containers/{container_id}.pid"
    assert not os.path.exists(pid_file), f"Container PID file {pid_file} still exists. The container was not properly stopped."
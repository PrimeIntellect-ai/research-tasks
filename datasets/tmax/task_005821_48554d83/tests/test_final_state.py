# test_final_state.py
import os
import json
import subprocess
import pytest

def test_metrics_agent_execution_and_output():
    # Run the wrapper script to ensure the agent works with the mock app
    run_script = "/home/user/run_all.sh"
    assert os.path.exists(run_script), f"{run_script} is missing."

    try:
        # This will take around 19 seconds due to mock_app.py sleeps
        result = subprocess.run([run_script], capture_output=True, text=True, timeout=30)
        assert result.returncode == 0, f"run_all.sh failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("run_all.sh timed out after 30 seconds. The metrics agent likely did not handle the startup dependency correctly.")

    dashboard_path = "/home/user/dashboard.json"
    assert os.path.exists(dashboard_path), f"Output file {dashboard_path} was not created."

    with open(dashboard_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{dashboard_path} does not contain valid JSON.")

    assert "storage_bytes" in data, "Key 'storage_bytes' missing from JSON."
    assert "default_gateway" in data, "Key 'default_gateway' missing from JSON."
    assert "status" in data, "Key 'status' missing from JSON."

    assert data["status"] == "active", f"Expected status 'active', got {data['status']}"
    assert isinstance(data["storage_bytes"], int), "storage_bytes must be an integer."
    assert isinstance(data["default_gateway"], str), "default_gateway must be a string."

    # Verify default gateway
    ip_route_cmd = subprocess.run(["ip", "route"], capture_output=True, text=True)
    expected_gateway = None
    for line in ip_route_cmd.stdout.splitlines():
        if line.startswith("default"):
            parts = line.split()
            if len(parts) >= 3:
                expected_gateway = parts[2]
                break

    if expected_gateway:
        assert data["default_gateway"] == expected_gateway, f"Expected default_gateway '{expected_gateway}', got '{data['default_gateway']}'"

    # Verify storage bytes
    # The agent should calculate the size of all files in /home/user/app_storage
    # Note: run_all.sh cleans up app.sock and app.log at the start, and mock_app.py creates them.
    # At the time metrics_agent runs, app.sock and app.log exist.
    # initial_data.bin = 1048576 bytes
    # app.log = 1000 bytes ("Log entry "*100)
    # app.sock = 13 bytes ("socket_active")
    # Total expected sum of file sizes = 1049589 bytes.
    # However, depending on how the student calculates (e.g., including directory size or not),
    # we allow a small variance or check if it matches the sum of file sizes exactly.

    expected_file_size_sum = 1048576 + 1000 + 13

    # We will accept either the exact file size sum, or the output of `du -sb` which includes the directory size.
    du_cmd = subprocess.run(["du", "-sb", "/home/user/app_storage"], capture_output=True, text=True)
    du_size = int(du_cmd.stdout.split()[0]) if du_cmd.returncode == 0 else expected_file_size_sum

    actual_storage = data["storage_bytes"]
    assert actual_storage == expected_file_size_sum or actual_storage == du_size, \
        f"Expected storage_bytes to be {expected_file_size_sum} (sum of files) or {du_size} (du -sb), but got {actual_storage}."
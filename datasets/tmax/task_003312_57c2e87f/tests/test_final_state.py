# test_final_state.py

import os
import json
import urllib.request
import pytest

def test_v2_directory_exists():
    v2_path = "/home/user/deploy/releases/v2"
    assert os.path.isdir(v2_path), f"Release directory not found at {v2_path}"

    # Check if there is an executable file in the v2 directory
    executables = [f for f in os.listdir(v2_path) if os.path.isfile(os.path.join(v2_path, f)) and os.access(os.path.join(v2_path, f), os.X_OK)]
    assert len(executables) > 0, f"No executable binary found in {v2_path}"

def test_symlink_updated():
    current_symlink = "/home/user/deploy/current"
    assert os.path.islink(current_symlink), f"{current_symlink} must be a symlink"

    target = os.readlink(current_symlink)
    # Allow absolute or relative symlinks as long as they resolve to the v2 directory
    resolved_target = os.path.realpath(current_symlink)
    expected_path = os.path.realpath("/home/user/deploy/releases/v2")

    assert resolved_target == expected_path, f"Symlink {current_symlink} should resolve to {expected_path}, but resolves to {resolved_target}"

def test_metrics_success_rate():
    metrics_path = "/home/user/metrics.txt"
    assert os.path.isfile(metrics_path), f"Metrics file not found at {metrics_path}. Did you run the load test script and pipe the output?"

    with open(metrics_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Metrics file {metrics_path} does not contain valid JSON.")

    assert "success_rate" in data, f"'success_rate' key not found in {metrics_path}"

    success_rate = data.get("success_rate", 0.0)
    assert isinstance(success_rate, (int, float)), "success_rate must be a number"
    assert success_rate >= 1.0, f"Expected success_rate >= 1.0, but got {success_rate}. The upstream service might not be handling all requests successfully."

def test_service_running_and_proxying():
    try:
        response = urllib.request.urlopen("http://127.0.0.1:8080", timeout=2)
        status_code = response.getcode()
        assert status_code == 200, f"Expected HTTP 200 from NGINX proxy, got {status_code}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"NGINX returned an HTTP error: {e.code} {e.reason}. The upstream service might still be broken or misconfigured.")
    except Exception as e:
        pytest.fail(f"Failed to connect to NGINX on port 8080: {e}")
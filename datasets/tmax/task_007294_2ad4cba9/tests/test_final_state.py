# test_final_state.py
import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_fallback_file():
    fallback_path = "/home/user/fallback.html"
    assert os.path.isfile(fallback_path), f"Fallback file not found: {fallback_path}"
    with open(fallback_path, "r") as f:
        content = f.read().strip()
    assert content == "Routed to cheap storage", f"Incorrect fallback file content: {content}"

def test_monitor_script_exists_and_executable():
    script_path = "/home/user/monitor_storage.sh"
    assert os.path.isfile(script_path), f"Monitor script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Monitor script is not executable: {script_path}"

def test_monitor_script_logic():
    script_path = "/home/user/monitor_storage.sh"
    fstab_path = "/home/user/cost_fstab"
    usage_path = "/home/user/expensive_usage.txt"

    # Run the script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Monitor script failed to execute: {result.stderr}"

    # Read the output
    assert os.path.isfile(usage_path), f"Usage file not created: {usage_path}"
    with open(usage_path, "r") as f:
        usage_str = f.read().strip()
    assert usage_str.isdigit(), f"Usage file does not contain a valid integer: {usage_str}"
    actual_usage = int(usage_str)

    # Calculate expected usage
    expected_usage = 0
    with open(fstab_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 4 and "tier=expensive" in parts[3]:
                path = parts[0]
                if os.path.isdir(path):
                    du_res = subprocess.run(["du", "-sb", path], capture_output=True, text=True)
                    if du_res.returncode == 0:
                        expected_usage += int(du_res.stdout.split()[0])

    assert actual_usage == expected_usage, f"Monitor script calculated {actual_usage}, expected {expected_usage}"

def test_quota_server_and_nginx_over_quota():
    usage_path = "/home/user/expensive_usage.txt"

    # Simulate over quota
    with open(usage_path, "w") as f:
        f.write("150000\n")

    # Test C server directly
    try:
        req = urllib.request.Request("http://127.0.0.1:9000")
        with urllib.request.urlopen(req, timeout=2) as response:
            pytest.fail("Expected 503 error from quota server, but got 200 OK")
    except urllib.error.HTTPError as e:
        assert e.code == 503, f"Expected 503 from quota server, got {e.code}"
        body = e.read().decode("utf-8").strip()
        assert "Quota Exceeded" in body, f"Expected 'Quota Exceeded' in body, got: {body}"
    except Exception as e:
        pytest.fail(f"Could not connect to quota server on port 9000: {e}")

    # Test Nginx proxy
    try:
        req = urllib.request.Request("http://127.0.0.1:8080")
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode("utf-8").strip()
            assert "Routed to cheap storage" in body, f"Expected fallback content, got: {body}"
    except urllib.error.HTTPError as e:
        if e.code == 503:
            pytest.fail("Nginx did not intercept the 503 error to serve fallback.html")
        else:
            pytest.fail(f"Nginx returned unexpected HTTP error: {e.code}")
    except Exception as e:
        pytest.fail(f"Could not connect to Nginx on port 8080: {e}")

def test_quota_server_and_nginx_under_quota():
    usage_path = "/home/user/expensive_usage.txt"

    # Simulate under quota
    with open(usage_path, "w") as f:
        f.write("50000\n")

    # Test C server directly
    try:
        req = urllib.request.Request("http://127.0.0.1:9000")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected 200 from quota server, got {response.status}"
            body = response.read().decode("utf-8").strip()
            assert "Traffic Allowed" in body, f"Expected 'Traffic Allowed' in body, got: {body}"
    except Exception as e:
        pytest.fail(f"Quota server request failed: {e}")

    # Test Nginx proxy
    try:
        req = urllib.request.Request("http://127.0.0.1:8080")
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected 200 from Nginx, got {response.status}"
            body = response.read().decode("utf-8").strip()
            assert "Traffic Allowed" in body, f"Expected 'Traffic Allowed' via Nginx, got: {body}"
    except Exception as e:
        pytest.fail(f"Nginx request failed: {e}")
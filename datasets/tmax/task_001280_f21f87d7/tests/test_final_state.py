# test_final_state.py

import os
import subprocess
import urllib.request
import socket
import pytest

def test_setup_tunnel_script_exists():
    path = "/home/user/setup_tunnel.py"
    assert os.path.exists(path), f"Expected script missing at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_load_test_script_exists():
    path = "/home/user/load_test.py"
    assert os.path.exists(path), f"Expected script missing at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_nginx_config_updated():
    path = "/home/user/nginx/nginx.conf"
    assert os.path.exists(path), f"Nginx config missing at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "9042" in content, "Nginx config does not appear to be updated with the correct port (9042)"

def test_port_9042_listening():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('localhost', 9042))
        assert result == 0, "Tunnel is not listening on port 9042"

def test_nginx_api_returns_200():
    url = "http://localhost:8080/api"
    try:
        response = urllib.request.urlopen(url)
        assert response.getcode() == 200, f"Expected 200 OK from {url}, got {response.getcode()}"
    except Exception as e:
        pytest.fail(f"Failed to connect to {url} or did not receive 200 OK: {e}")

def test_load_test_success_rate():
    path = "/home/user/load_test.py"
    try:
        result = subprocess.run(
            ["python3", path],
            capture_output=True,
            text=True,
            check=True,
            timeout=15
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Executing {path} failed with return code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Executing {path} timed out after 15 seconds")

    output = result.stdout.strip()
    try:
        success_rate = float(output)
    except ValueError:
        pytest.fail(f"Output of {path} could not be parsed as a float. Output was: {output!r}")

    assert success_rate >= 1.0, f"Expected success_rate >= 1.0, got {success_rate}"
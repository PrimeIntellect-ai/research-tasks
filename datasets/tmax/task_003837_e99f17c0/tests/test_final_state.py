# test_final_state.py

import os
import requests

def test_deploy_script_exists_and_executable():
    path = "/home/user/deploy.sh"
    assert os.path.isfile(path), f"Deployment script missing at {path}"
    assert os.access(path, os.X_OK), f"Deployment script at {path} is not executable (missing +x)"

def test_deploy_script_contents():
    path = "/home/user/deploy.sh"
    with open(path, 'r') as f:
        content = f.read()

    assert "server" in content, "Deployment script does not seem to reference the Rust server binary"
    assert "nginx" in content, "Deployment script does not seem to reference nginx"
    assert "reload" in content, "Deployment script does not seem to perform an nginx reload"

def test_health_endpoint():
    url = "http://127.0.0.1:8080/health"
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

        data = response.json()
        assert data == {"status": "ok"}, f"Expected JSON {{'status': 'ok'}}, got {data}"
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to {url} or request failed: {e}"
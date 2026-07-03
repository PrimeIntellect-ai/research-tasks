# test_final_state.py
import json
import os
import requests
import pytest

def test_roles_json_exists_and_valid():
    path = "/home/user/roles.json"
    assert os.path.exists(path), f"{path} does not exist"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not valid JSON")

    assert "users" in data, "Key 'users' missing in roles.json"
    assert "release_bot" in data["users"], "User 'release_bot' missing in roles.json"
    assert data["users"]["release_bot"].get("group") == "deployment_admins", "User 'release_bot' is not in 'deployment_admins' group"

def test_deploy_exp_exists():
    path = "/home/user/deploy.exp"
    assert os.path.exists(path), f"{path} does not exist"

def test_rust_project_exists():
    path = "/home/user/gateway/Cargo.toml"
    assert os.path.exists(path), f"Rust project Cargo.toml not found at {path}"

def test_gateway_unauthorized():
    url = "http://127.0.0.1:8181/deploy"
    headers = {"Content-Type": "application/json"}
    body = {"username": "release_bot"}

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=5)
        assert resp.status_code == 401, f"Expected 401 Unauthorized for missing auth token, got {resp.status_code}. Response: {resp.text}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to gateway service: {e}")

def test_gateway_forbidden():
    url = "http://127.0.0.1:8181/deploy"
    headers = {
        "Authorization": "Bearer S3cr3t_R0ll0ut",
        "Content-Type": "application/json"
    }
    body = {"username": "unknown_user"}

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=5)
        assert resp.status_code == 403, f"Expected 403 Forbidden for unknown user, got {resp.status_code}. Response: {resp.text}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to gateway service: {e}")

def test_gateway_success():
    url = "http://127.0.0.1:8181/deploy"
    headers = {
        "Authorization": "Bearer S3cr3t_R0ll0ut",
        "Content-Type": "application/json"
    }
    body = {"username": "release_bot"}

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=10)
        assert resp.status_code == 200, f"Expected 200 OK for valid request, got {resp.status_code}. Response: {resp.text}"

        try:
            data = resp.json()
        except ValueError:
            pytest.fail(f"Expected JSON response, got: {resp.text}")

        assert data.get("status") == "deployed", f"Expected {{'status': 'deployed'}}, got {data}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to gateway service: {e}")
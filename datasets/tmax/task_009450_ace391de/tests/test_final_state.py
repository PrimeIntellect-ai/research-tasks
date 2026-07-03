# test_final_state.py

import os
import json
import socket
import pytest

def test_backup_and_convert_script():
    script_path = "/home/user/backup_and_convert.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_backup_exists():
    backup_path = "/home/user/backups/legacy_proxy.conf.bak"
    assert os.path.exists(backup_path), f"Backup file {backup_path} does not exist."
    with open(backup_path, "r") as f:
        content = f.read()
    assert "route_api=18080" in content, "Backup file missing route_api."
    assert "route_web=18081" in content, "Backup file missing route_web."
    assert "route_metrics=18082" in content, "Backup file missing route_metrics."

def test_new_proxy_json():
    json_path = "/home/user/new_proxy.json"
    assert os.path.exists(json_path), f"JSON file {json_path} does not exist."
    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "routes" in data, "JSON missing 'routes' key."
    routes = data["routes"]
    assert isinstance(routes, list), "'routes' should be a list."

    expected_routes = {
        "route_api": 18080,
        "route_web": 18081,
        "route_metrics": 18082
    }

    actual_routes = {r.get("name"): r.get("port") for r in routes if isinstance(r, dict)}

    for name, port in expected_routes.items():
        assert name in actual_routes, f"Route {name} missing in JSON."
        assert actual_routes[name] == port, f"Route {name} has incorrect port in JSON (expected {port}, got {actual_routes[name]})."
        assert isinstance(actual_routes[name], int), f"Port for {name} should be an integer."

def test_rust_project_exists():
    cargo_toml = "/home/user/proxy_service/Cargo.toml"
    assert os.path.exists(cargo_toml), f"Rust project not found at {cargo_toml}."

def test_deploy_script():
    script_path = "/home/user/deploy.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_migration_status():
    status_path = "/home/user/migration_status.txt"
    assert os.path.exists(status_path), f"Status file {status_path} does not exist."
    with open(status_path, "r") as f:
        content = f.read().strip()
    assert content == "status=MIGRATED", f"Status file content incorrect. Got: {content}"

def test_proxy_log():
    log_path = "/home/user/proxy.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()

    assert "Started route_api on 18080" in content, "Missing api log."
    assert "Started route_web on 18081" in content, "Missing web log."
    assert "Started route_metrics on 18082" in content, "Missing metrics log."

def test_ports_bound():
    ports = [18080, 18081, 18082]
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # If connect succeeds, the port is bound and listening
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"Port {port} is not bound."
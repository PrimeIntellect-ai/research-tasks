# test_final_state.py
import os
import json
import socket
import pytest

def test_app_config_exists_and_valid():
    """Check that app_config.json exists and contains the expected services."""
    config_path = "/home/user/app_config.json"
    assert os.path.exists(config_path), f"{config_path} does not exist."

    with open(config_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{config_path} is not valid JSON.")

    assert "services" in data, "Key 'services' not found in app_config.json."
    services = data["services"]
    assert len(services) >= 2, "Expected at least 2 services in app_config.json."

    service_names = [s.get("name") for s in services]
    assert "auth_service" in service_names, "auth_service missing from config."
    assert "data_service" in service_names, "data_service missing from config."

def test_mock_scripts_exist():
    """Check that the mock service scripts were created."""
    assert os.path.exists("/home/user/mock_auth.py"), "/home/user/mock_auth.py is missing."
    assert os.path.exists("/home/user/mock_data.py"), "/home/user/mock_data.py is missing."

def test_health_monitor_exists():
    """Check that the health monitor script was created."""
    assert os.path.exists("/home/user/health_monitor.py"), "/home/user/health_monitor.py is missing."

def test_status_csv_content():
    """Check that status.csv contains exactly the expected sequence of states."""
    csv_path = "/home/user/status.csv"
    assert os.path.exists(csv_path), f"{csv_path} does not exist."

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "auth_service,RESTARTED",
        "data_service,RESTARTED",
        "auth_service,UP",
        "data_service,UP"
    ]

    assert lines == expected_lines, f"Contents of {csv_path} do not match expected output. Got: {lines}"

def test_ports_listening():
    """Check that ports 9010 and 9011 are actively listening on localhost."""
    for port in [9010, 9011]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"Port {port} is not actively accepting connections."
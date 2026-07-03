# test_final_state.py

import os
import json
import configparser
import pytest

def test_rust_binary_exists():
    binary_path = "/home/user/quota_app/target/release/quota_app"
    assert os.path.isfile(binary_path), f"Rust release binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Rust binary at {binary_path} is not executable"

def test_systemd_service_file():
    service_path = "/home/user/.config/systemd/user/quota-monitor.service"
    assert os.path.isfile(service_path), f"Systemd service file not found at {service_path}"

    config = configparser.ConfigParser()
    # systemd files can sometimes have options without values, but configparser should handle basic ones
    # Strict=False to allow duplicate keys if any, though there shouldn't be
    try:
        config.read(service_path)
    except Exception as e:
        pytest.fail(f"Could not parse systemd service file: {e}")

    assert "Unit" in config, "Missing [Unit] section in service file"
    assert config["Unit"].get("Description") == "Quota Monitor", "Incorrect Description in [Unit]"

    assert "Service" in config, "Missing [Service] section in service file"
    assert config["Service"].get("ExecStart") == "/home/user/quota_app/target/release/quota_app", "Incorrect ExecStart in [Service]"
    assert config["Service"].get("Restart") == "always", "Incorrect Restart in [Service]"

    assert "Install" in config, "Missing [Install] section in service file"
    assert config["Install"].get("WantedBy") == "default.target", "Incorrect WantedBy in [Install]"

def test_deployment_verification_log():
    log_path = "/home/user/deployment_verification.log"
    assert os.path.isfile(log_path), f"Log file not found at {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of {log_path} is not valid JSON")

    assert isinstance(data, list), "JSON output must be an array"

    # Check alice
    alice_data = next((item for item in data if item.get("user") == "alice"), None)
    assert alice_data is not None, "Missing data for user 'alice' in JSON output"
    assert alice_data.get("usage") == 1500, "Incorrect usage for 'alice'"
    assert alice_data.get("exceeded") is True, "Incorrect exceeded status for 'alice'"

    # Check bob
    bob_data = next((item for item in data if item.get("user") == "bob"), None)
    assert bob_data is not None, "Missing data for user 'bob' in JSON output"
    assert bob_data.get("usage") == 2000, "Incorrect usage for 'bob'"
    assert bob_data.get("exceeded") is False, "Incorrect exceeded status for 'bob'"
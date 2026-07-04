# test_final_state.py

import os
import json
import pytest

def test_executable_compiled():
    """Check that the C++ API server has been compiled and is executable."""
    executable_path = "/home/user/cost_api"
    assert os.path.isfile(executable_path), f"Executable '{executable_path}' does not exist. Did you compile the C++ code?"
    assert os.access(executable_path, os.X_OK), f"File '{executable_path}' is not executable."

def test_tls_certificates_exist():
    """Check that the TLS certificates have been generated."""
    key_path = "/home/user/key.pem"
    cert_path = "/home/user/cert.pem"
    assert os.path.isfile(key_path), f"Private key '{key_path}' does not exist."
    assert os.path.isfile(cert_path), f"Certificate '{cert_path}' does not exist."

def test_api_service_file():
    """Check that the API systemd service file is created correctly."""
    service_path = "/home/user/.config/systemd/user/cost-api.service"
    assert os.path.isfile(service_path), f"Service file '{service_path}' does not exist."
    with open(service_path, "r") as f:
        content = f.read()
    assert "/home/user/cost_api" in content, "The API service does not execute '/home/user/cost_api'."
    assert "Restart=always" in content or "Restart= always" in content, "The API service is not configured to restart always."
    assert "WorkingDirectory=/home/user" in content, "The API service does not set WorkingDirectory=/home/user."

def test_reporter_service_file():
    """Check that the reporter systemd service file is configured correctly."""
    service_path = "/home/user/.config/systemd/user/cost-reporter.service"
    assert os.path.isfile(service_path), f"Service file '{service_path}' does not exist."
    with open(service_path, "r") as f:
        content = f.read()
    assert "Type=oneshot" in content, "The reporter service is not configured as Type=oneshot."
    assert "/home/user/reporter.sh" in content, "The reporter service does not execute '/home/user/reporter.sh'."
    assert "After=cost-api.service" in content, "The reporter service does not contain 'After=cost-api.service'."
    assert "Requires=cost-api.service" in content or "Wants=cost-api.service" in content, "The reporter service does not Require or Want 'cost-api.service'."

def test_metrics_log_created_and_valid():
    """Check that the metrics.log was successfully created and contains the expected JSON."""
    log_path = "/home/user/metrics.log"
    assert os.path.isfile(log_path), f"Log file '{log_path}' does not exist. The service might not have started or the reporter failed."

    with open(log_path, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"Content of '{log_path}' is not valid JSON: {content}")

    expected_data = {"instance": "i-0abcd1234", "spot_price": 0.045, "region": "us-east-1"}
    assert data == expected_data, f"Log file content does not match expected payload. Found: {data}"
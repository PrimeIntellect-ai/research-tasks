# test_final_state.py

import os
import json
import socket

def test_config_updated():
    config_path = '/home/user/config.json'
    assert os.path.isfile(config_path), f"Configuration file {config_path} is missing."

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Configuration file {config_path} is no longer valid JSON."

    assert config.get('port') == 8443, f"Expected port in config to be 8443, got {config.get('port')}."

def test_certificates_exist():
    cert_path = '/home/user/cert.pem'
    key_path = '/home/user/key.pem'

    assert os.path.isfile(cert_path), "Certificate file cert.pem was not created."
    assert os.path.getsize(cert_path) > 0, "Certificate file cert.pem is empty."

    assert os.path.isfile(key_path), "Private key file key.pem was not created."
    assert os.path.getsize(key_path) > 0, "Private key file key.pem is empty."

def test_health_check_output():
    health_path = '/home/user/health_check.txt'
    assert os.path.isfile(health_path), f"Health check output file {health_path} was not created."

    with open(health_path, 'r') as f:
        content = f.read().strip()

    assert content == '{"status": "ok"}', f"Expected health check output to be '{{\"status\": \"ok\"}}', got '{content}'."

def test_server_listening():
    # Check if a process is listening on port 8443
    is_listening = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)
        result = s.connect_ex(('127.0.0.1', 8443))
        if result == 0:
            is_listening = True

    assert is_listening, "No service is listening on 127.0.0.1:8443. The server might not be running or failed to start."
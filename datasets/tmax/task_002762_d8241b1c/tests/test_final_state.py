# test_final_state.py

import os
import socket
import requests
import pytest

def test_service_file_updated():
    path = "/home/user/.config/systemd/user/voicemail-api.service"
    assert os.path.isfile(path), f"Service file missing at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "Europe/Zurich" in content, "Timezone Europe/Zurich not found in service file"
    assert "fr_CH.UTF-8" in content, "Locale fr_CH.UTF-8 not found in service file"

def test_server_script_updated():
    path = "/home/user/app/server.py"
    assert os.path.isfile(path), f"Server script missing at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "Authorization code delta seven nine omega." in content, "Transcript text not updated in server.py"

def test_grpc_port_listening():
    # Check if gRPC port 50051 is open
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 50051))
    sock.close()
    assert result == 0, "gRPC port 50051 is not listening. Is the service running?"

def test_http_endpoint_via_ssh_tunnel():
    # Check if HTTP endpoint is accessible via SSH tunnel on port 9090
    url = "http://127.0.0.1:9090/transcript"
    headers = {"Authorization": "Bearer voicemail-admin"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to http://127.0.0.1:9090. Is the SSH tunnel active?")
    except requests.exceptions.Timeout:
        pytest.fail("Request to http://127.0.0.1:9090 timed out.")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_transcript = "Authorization code delta seven nine omega."
    assert data.get("transcript") == expected_transcript, f"Incorrect transcript: {data.get('transcript')}"
    assert data.get("tz") == "Europe/Zurich", f"Incorrect timezone: {data.get('tz')}"
    assert data.get("locale") == "fr_CH.UTF-8", f"Incorrect locale: {data.get('locale')}"
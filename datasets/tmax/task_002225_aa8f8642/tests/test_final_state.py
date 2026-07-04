# test_final_state.py

import os
import json
import socket
import pytest
import requests

def test_deploy_script_exists_and_executable():
    path = "/home/user/deploy.sh"
    assert os.path.exists(path), f"Deployment script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"Deployment script {path} is not executable."

def test_backups_directory_exists():
    path = "/home/user/backups/"
    assert os.path.exists(path), f"Backup directory {path} does not exist."
    assert os.path.isdir(path), f"{path} is not a directory."

def test_backend_conf_exists_and_valid():
    path = "/home/user/backend.conf"
    assert os.path.exists(path), f"Config file {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "HTTP_PORT=8080" in content, "HTTP_PORT=8080 not found in backend.conf"
    assert "TCP_PORT=8081" in content, "TCP_PORT=8081 not found in backend.conf"
    assert "INCIDENT_FILE=/home/user/incident_text.txt" in content, "INCIDENT_FILE path not found in backend.conf"

def check_transcription_keywords(text):
    text_lower = text.lower()
    keywords = ["database", "connection", "timeout", "eu", "west"]
    for kw in keywords:
        assert kw in text_lower, f"Expected keyword '{kw}' not found in transcription: {text}"

def test_http_server_response():
    try:
        response = requests.get("http://127.0.0.1:8080/", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert "incident" in data, "JSON response missing 'incident' key."
    check_transcription_keywords(data["incident"])

def test_tcp_server_response():
    try:
        with socket.create_connection(("127.0.0.1", 8081), timeout=2) as s:
            data = s.recv(4096)
    except Exception as e:
        pytest.fail(f"Failed to connect to TCP server on port 8081: {e}")

    assert data, "Received empty response from TCP server."
    text = data.decode("utf-8")
    assert text.endswith("\n"), "TCP response does not end with a newline."
    check_transcription_keywords(text)
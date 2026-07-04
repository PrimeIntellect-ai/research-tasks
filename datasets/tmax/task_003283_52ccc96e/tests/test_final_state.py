# test_final_state.py

import socket
import json
import pytest

def send_request(host, port, payload):
    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(payload.encode('utf-8'))
            response = s.recv(4096).decode('utf-8')
            return response
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with the server at {host}:{port}. Error: {e}")

def test_tcp_server_node_101():
    host = '127.0.0.1'
    port = 8080
    payload = "101\n"

    response = send_request(host, port, payload)
    assert response, "Received empty response from the server"

    try:
        data = json.loads(response.strip())
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response}")

    assert "node" in data, "Response JSON missing 'node' key"
    assert "score" in data, "Response JSON missing 'score' key"

    assert data["node"] == 101, f"Expected node 101, got {data['node']}"
    assert data["score"] == 367, f"Expected score 367 for node 101, got {data['score']}"

def test_tcp_server_node_102():
    host = '127.0.0.1'
    port = 8080
    payload = "102\n"

    response = send_request(host, port, payload)
    assert response, "Received empty response from the server"

    try:
        data = json.loads(response.strip())
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response}")

    assert "node" in data, "Response JSON missing 'node' key"
    assert "score" in data, "Response JSON missing 'score' key"

    assert data["node"] == 102, f"Expected node 102, got {data['node']}"
    assert data["score"] == 334, f"Expected score 334 for node 102, got {data['score']}"
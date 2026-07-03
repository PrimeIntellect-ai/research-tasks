# test_final_state.py

import os
import json
import socket
import subprocess
import pytest
import requests

def test_success_log_exists():
    path = "/tmp/success.log"
    assert os.path.isfile(path), f"Expected success log at {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert "READY" in content, f"Expected 'READY' in {path}, but got '{content}'."

def test_legacy_schema_dumped():
    path = "/tmp/legacy_schema.json"
    assert os.path.isfile(path), f"Expected dumped schema at {path} is missing."
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    assert isinstance(data, list), f"Expected JSON array in {path}."
    assert len(data) == 4, f"Expected 4 nodes in {path}, got {len(data)}."

def test_http_migrate_endpoint():
    url = "http://127.0.0.1:8080/migrate"
    try:
        response = requests.post(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to POST {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK from POST {url}, got {response.status_code}. Body: {response.text}"

def test_redis_ordered_nodes():
    try:
        result = subprocess.run(
            ["redis-cli", "GET", "v2:ordered_nodes"],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run redis-cli: {e.stderr}")

    output = result.stdout.strip()
    assert output != "", "Key v2:ordered_nodes is empty or does not exist."

    try:
        ordered_nodes = json.loads(output)
    except json.JSONDecodeError:
        pytest.fail(f"v2:ordered_nodes is not valid JSON: {output}")

    expected_order = ["node_C", "node_B", "node_A", "node_D"]
    assert ordered_nodes == expected_order, f"Expected topological sort {expected_order}, got {ordered_nodes}."

@pytest.mark.parametrize("node_id, expected_asm", [
    ("node_A", "PUSH ADD"),
    ("node_B", "PUSH PUSH ADD"),
    ("node_C", "NOP"),
    ("node_D", "POP POP"),
])
def test_http_get_node_endpoint(node_id, expected_asm):
    url = f"http://127.0.0.1:8080/node/{node_id}"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to GET {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK from GET {url}, got {response.status_code}. Body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from GET {url} is not valid JSON: {response.text}")

    assert data.get("id") == node_id, f"Expected node id {node_id}, got {data.get('id')}."
    assert data.get("asm") == expected_asm, f"Expected asm '{expected_asm}' for {node_id}, got '{data.get('asm')}'."

@pytest.mark.parametrize("node_id, expected_asm", [
    ("node_A", "PUSH ADD"),
    ("node_B", "PUSH PUSH ADD"),
    ("node_C", "NOP"),
    ("node_D", "POP POP"),
])
def test_tcp_endpoint(node_id, expected_asm):
    host = "127.0.0.1"
    port = 9000

    try:
        with socket.create_connection((host, port), timeout=5) as s:
            s.sendall(f"{node_id}\n".encode("utf-8"))
            response = s.recv(1024).decode("utf-8")
    except Exception as e:
        pytest.fail(f"Failed to communicate with TCP server at {host}:{port}: {e}")

    assert response.strip() == expected_asm, f"Expected '{expected_asm}' from TCP server for {node_id}, got '{response.strip()}'."
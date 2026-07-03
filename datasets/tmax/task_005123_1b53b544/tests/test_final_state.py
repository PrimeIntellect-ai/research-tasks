# test_final_state.py

import os
import json
import socket
import requests
import pytest

def test_makefile_fixed():
    makefile_path = '/app/vendor/pcap-processor/Makefile'
    assert os.path.isfile(makefile_path), f"File {makefile_path} does not exist"
    with open(makefile_path, 'r') as f:
        content = f.read()
    assert 'PYTHONPATH=/wrong/path' not in content, "Makefile still contains the wrong PYTHONPATH"

def test_mre_script_exists():
    mre_path = '/home/user/mre.py'
    assert os.path.isfile(mre_path), f"MRE script {mre_path} does not exist"

def test_http_endpoint_stats():
    try:
        response = requests.get('http://127.0.0.1:8080/stats', timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get('tcp_count') == 10000, f"Expected tcp_count=10000, got {data.get('tcp_count')}"
    assert data.get('udp_count') == 5000, f"Expected udp_count=5000, got {data.get('udp_count')}"

def test_tcp_endpoint_tcp_query():
    try:
        with socket.create_connection(('127.0.0.1', 8081), timeout=2) as s:
            s.sendall(b'{"query": "tcp"}\n')
            response = s.recv(4096).decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with TCP server on port 8081: {e}")

    try:
        data = json.loads(response)
    except ValueError:
        pytest.fail(f"TCP response is not valid JSON: {response}")

    assert data.get('count') == 10000, f"Expected count=10000 for tcp query, got {data.get('count')}"

def test_tcp_endpoint_udp_query():
    try:
        with socket.create_connection(('127.0.0.1', 8081), timeout=2) as s:
            s.sendall(b'{"query": "udp"}\n')
            response = s.recv(4096).decode('utf-8').strip()
    except Exception as e:
        pytest.fail(f"Failed to connect or communicate with TCP server on port 8081: {e}")

    try:
        data = json.loads(response)
    except ValueError:
        pytest.fail(f"TCP response is not valid JSON: {response}")

    assert data.get('count') == 5000, f"Expected count=5000 for udp query, got {data.get('count')}"
# test_final_state.py

import os
import socket
import tarfile
import zipfile
import tempfile
import requests

def redis_get(key):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(('127.0.0.1', 6379))
        s.sendall(f"GET {key}\r\n".encode())
        resp = s.recv(1024).decode()
        s.close()
        lines = resp.split('\r\n')
        if lines[0].startswith('$'):
            return lines[1]
        return None
    except Exception as e:
        return None

def extract_original_data():
    tmpdir = tempfile.mkdtemp()
    with tarfile.open('/app/dataset.tar.gz', 'r:gz') as tar:
        tar.extractall(path=tmpdir)

    for sensor in ['sensor_alpha', 'sensor_beta']:
        zip_path = os.path.join(tmpdir, f"{sensor}.zip")
        if os.path.exists(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(path=tmpdir)
    return tmpdir

def test_redis_chunk_counts():
    """Verify that Redis contains the correct chunk counts for both sensors."""
    alpha_count = redis_get("sensor_chunks:sensor_alpha")
    assert alpha_count == "3", f"Expected Redis key sensor_chunks:sensor_alpha to be '3', got '{alpha_count}'"

    beta_count = redis_get("sensor_chunks:sensor_beta")
    assert beta_count == "2", f"Expected Redis key sensor_chunks:sensor_beta to be '2', got '{beta_count}'"

def test_api_meta_endpoint():
    """Verify the Nginx reverse proxy and Go server return the correct metadata."""
    try:
        resp = requests.get("http://127.0.0.1:8090/api/data/sensor_alpha/meta", timeout=2)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to Nginx gateway on port 8090: {e}"

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    assert resp.text.strip() == "Alpha-v1.2 active", f"Unexpected meta content: {resp.text}"

    resp = requests.get("http://127.0.0.1:8090/api/data/sensor_beta/meta", timeout=2)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    assert resp.text.strip() == "Beta-v2.0 inactive", f"Unexpected meta content: {resp.text}"

def test_api_chunk_endpoint():
    """Verify the Nginx reverse proxy and Go server return the correct binary chunk data."""
    tmpdir = extract_original_data()

    alpha_data_path = os.path.join(tmpdir, 'sensor_alpha', 'data.bin')
    assert os.path.exists(alpha_data_path), "Could not extract sensor_alpha/data.bin for validation"
    with open(alpha_data_path, 'rb') as f:
        alpha_data = f.read()

    try:
        resp = requests.get("http://127.0.0.1:8090/api/data/sensor_alpha/chunk/1", timeout=2)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to fetch chunk: {e}"

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    expected_alpha_chunk = alpha_data[1000000:2000000]
    assert resp.content == expected_alpha_chunk, "Binary data for sensor_alpha chunk 1 does not match the original dataset"

    beta_data_path = os.path.join(tmpdir, 'sensor_beta', 'data.bin')
    assert os.path.exists(beta_data_path), "Could not extract sensor_beta/data.bin for validation"
    with open(beta_data_path, 'rb') as f:
        beta_data = f.read()

    resp = requests.get("http://127.0.0.1:8090/api/data/sensor_beta/chunk/1", timeout=2)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    expected_beta_chunk = beta_data[1000000:2000000]
    assert resp.content == expected_beta_chunk, "Binary data for sensor_beta chunk 1 does not match the original dataset"
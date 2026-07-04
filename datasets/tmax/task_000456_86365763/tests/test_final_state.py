# test_final_state.py

import os
import json
import gzip
import time
import requests
import pytest
from concurrent.futures import ThreadPoolExecutor

PORT = 8118
HOST = "127.0.0.1"
API_TOKEN = "AlphaBravoCharlie99"
ACTIVE_CONFIGS_DIR = "/home/user/active_configs"
CHANGELOG_FILE = "/home/user/system_changelog.log"

def wait_for_service():
    """Wait for the service to be reachable."""
    max_retries = 30
    for _ in range(max_retries):
        try:
            # Just test if the port is open by attempting a connection
            import socket
            with socket.create_connection((HOST, PORT), timeout=1):
                return True
        except (socket.timeout, socket.error):
            time.sleep(1)
    return False

@pytest.fixture(scope="module", autouse=True)
def setup_service():
    assert wait_for_service(), f"Service is not listening on {HOST}:{PORT}"

def test_legacy_migration():
    """Verify that legacy configs were correctly migrated and renamed."""
    expected_files = [
        "auth_svc_v2.json.gz",
        "payment_gw_v1.json.gz"
    ]
    for filename in expected_files:
        filepath = os.path.join(ACTIVE_CONFIGS_DIR, filename)
        assert os.path.isfile(filepath), f"Legacy config not found at {filepath}"

        # Verify it's a valid gzip and contains correct JSON
        try:
            with gzip.open(filepath, 'rt') as f:
                data = json.load(f)
                assert "service_name" in data
                assert "version" in data
        except Exception as e:
            pytest.fail(f"Failed to read {filepath} as gzipped JSON: {e}")

def test_unauthorized_request():
    """Verify that requests without the correct token are rejected."""
    url = f"http://{HOST}:{PORT}/upload"
    payload = {"service_name": "test_unauth", "version": 1, "settings": {}}
    gzipped_payload = gzip.compress(json.dumps(payload).encode('utf-8'))

    response = requests.post(url, data=gzipped_payload)
    assert response.status_code == 401, "Expected 401 Unauthorized for missing token"

    headers = {"Authorization": "Bearer WrongToken123"}
    response = requests.post(url, data=gzipped_payload, headers=headers)
    assert response.status_code == 401, "Expected 401 Unauthorized for incorrect token"

def test_upload_and_concurrency():
    """Verify that concurrent uploads work and changelog is locked correctly."""
    url = f"http://{HOST}:{PORT}/upload"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def upload_config(i):
        service_name = f"concurrent_svc_{i}"
        version = i
        payload = {"service_name": service_name, "version": version, "settings": {"index": i}}
        gzipped_payload = gzip.compress(json.dumps(payload).encode('utf-8'))

        response = requests.post(url, data=gzipped_payload, headers=headers)
        return response.status_code, service_name, version

    num_requests = 10
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(upload_config, range(num_requests)))

    for status, svc, ver in results:
        assert status == 200, f"Expected 200 OK for {svc}, got {status}"

        # Verify file exists
        filepath = os.path.join(ACTIVE_CONFIGS_DIR, f"{svc}_v{ver}.json.gz")
        assert os.path.isfile(filepath), f"Uploaded config not found at {filepath}"

        # Verify content
        with gzip.open(filepath, 'rt') as f:
            data = json.load(f)
            assert data["service_name"] == svc
            assert data["version"] == ver

    # Verify changelog
    assert os.path.isfile(CHANGELOG_FILE), f"Changelog file missing at {CHANGELOG_FILE}"
    with open(CHANGELOG_FILE, 'r') as f:
        lines = f.readlines()

    # Check for interleaved lines or malformed lines
    for line in lines:
        assert line.startswith("UPDATED ") and " TO v" in line and line.endswith("\n"), f"Malformed changelog line: {repr(line)}"

    # Ensure all concurrent requests were logged
    for _, svc, ver in results:
        expected_log = f"UPDATED {svc} TO v{ver}\n"
        assert expected_log in lines, f"Missing log entry for {svc} in changelog"
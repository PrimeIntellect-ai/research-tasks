# test_final_state.py

import json
import os
import socket
import urllib.request
import urllib.error
import pytest

def test_result_file_exists_and_correct():
    """Verify the result file exists and contains the correct base64 encoded string."""
    filepath = "/home/user/test_result.json"
    assert os.path.isfile(filepath), f"Expected result file not found at {filepath}"

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} does not contain valid JSON")

    assert "result" in data, "JSON response missing 'result' key"
    expected_result = "V3l2cXhsYS1FOiBLbG1sdWsgQW9sIEp2eWwh"
    assert data["result"] == expected_result, f"Expected result '{expected_result}', but got '{data['result']}'"

def test_ports_listening():
    """Verify that processes are listening on ports 3000 (Rust) and 8080 (Nginx)."""
    for port, service in [(3000, "Rust API"), (8080, "Nginx Proxy")]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"{service} is not listening on 127.0.0.1:{port}"

def test_nginx_proxy_functionality():
    """Test the Nginx reverse proxy endpoint with a custom payload."""
    url = "http://127.0.0.1:8080/v1/telemetry"
    payload = {"text": "abc", "shift": 1}
    data = json.dumps(payload).encode('utf-8')

    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            try:
                resp_json = json.loads(body)
            except json.JSONDecodeError:
                pytest.fail("API response is not valid JSON")

            assert "result" in resp_json, "API response missing 'result' key"
            expected_result = "YmNk" # base64 for 'bcd'
            assert resp_json["result"] == expected_result, f"Expected API result '{expected_result}', got '{resp_json['result']}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy at {url}: {e}")
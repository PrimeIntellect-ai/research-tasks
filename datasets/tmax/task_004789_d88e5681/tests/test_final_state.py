# test_final_state.py

import os
import json
import io
import sys
import importlib.util
import pytest

def test_audit_report():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"Audit report missing at {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Audit report is not valid JSON")

    assert data.get("attacker_ip") == "198.51.100.42", "Incorrect attacker_ip in audit report"
    assert data.get("compromised_file") == "/home/user/.bashrc", "Incorrect compromised_file in audit report"

def get_flask_app():
    server_path = "/home/user/app/server.py"
    assert os.path.isfile(server_path), f"Server file missing at {server_path}"

    spec = importlib.util.spec_from_file_location("server", server_path)
    server_module = importlib.util.module_from_spec(spec)
    sys.modules["server"] = server_module
    try:
        spec.loader.exec_module(server_module)
    except Exception as e:
        pytest.fail(f"Failed to load server.py: {e}")

    assert hasattr(server_module, "app"), "Flask 'app' object not found in server.py"
    return server_module.app

def test_waf_ip_block():
    app = get_flask_app()
    client = app.test_client()

    # Test blocked IP
    response = client.get('/', environ_base={'REMOTE_ADDR': '198.51.100.42'})
    assert response.status_code == 403, "Expected HTTP 403 Forbidden for blocked IP"
    assert b"Blocked IP" in response.data, "Expected 'Blocked IP' text in response for blocked IP"

    # Test allowed IP
    response = client.get('/upload', environ_base={'REMOTE_ADDR': '10.0.0.5'})
    # It might return 400 or 405 depending on method, but shouldn't be the WAF 403
    if response.status_code == 403:
        assert b"Blocked IP" not in response.data, "Normal IP was incorrectly blocked by WAF"

def test_waf_traversal_block():
    app = get_flask_app()
    client = app.test_client()

    # Test blocked traversal in URL path
    response = client.get('/some/../test')
    assert response.status_code == 403, "Expected HTTP 403 Forbidden for path traversal in URL"
    assert b"Blocked Traversal" in response.data, "Expected 'Blocked Traversal' text in response"

    # URL encoded version
    response = client.get('/some/%2e%2e/test')
    if response.status_code == 403:
        assert b"Blocked Traversal" in response.data, "Expected 'Blocked Traversal' text in response"

def test_upload_remediation():
    app = get_flask_app()
    client = app.test_client()

    target_escape_file = "/home/user/test_escape_remediation.txt"
    if os.path.exists(target_escape_file):
        os.remove(target_escape_file)

    data = {
        'file': (io.BytesIO(b"malicious content"), "../../../home/user/test_escape_remediation.txt"),
        'filename': "../../../home/user/test_escape_remediation.txt"
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data')

    # Assert the file wasn't written outside the uploads directory
    assert not os.path.exists(target_escape_file), "Vulnerability still exists: file was written outside the uploads directory!"

    # If it was saved securely, it should be in /home/user/app/uploads/
    secure_path = "/home/user/app/uploads/test_escape_remediation.txt"
    if os.path.exists(secure_path):
        os.remove(secure_path)
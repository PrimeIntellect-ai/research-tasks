# test_final_state.py
import os
import sys
import importlib.util
from unittest.mock import patch

def test_report_contents():
    report_path = "/home/user/report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    assert len(lines) >= 3, f"Report file {report_path} must contain at least 3 lines."

    assert lines[0] == "CWE-601", f"Line 1 of report is '{lines[0]}', expected 'CWE-601'."
    assert lines[1] == "EvilCorpRoot", f"Line 2 of report is '{lines[1]}', expected 'EvilCorpRoot'."
    assert lines[2] == "/home/user/secret_master_key.pem", f"Line 3 of report is '{lines[2]}', expected '/home/user/secret_master_key.pem'."

def test_server_patched():
    server_path = "/home/user/evidence/server.py"
    assert os.path.isfile(server_path), f"{server_path} is missing."

    # Load the Flask app to test the patch
    spec = importlib.util.spec_from_file_location("server", server_path)
    server_module = importlib.util.module_from_spec(spec)
    sys.modules["server"] = server_module
    spec.loader.exec_module(server_module)

    app = getattr(server_module, "app", None)
    assert app is not None, "Flask app not found in server.py"

    client = app.test_client()

    # Test valid relative redirect
    response = client.post('/login?next=/dashboard')
    assert response.status_code == 302, "Valid relative redirect did not return 302."
    assert response.headers['Location'] == '/dashboard', "Valid relative redirect failed."

    # Test invalid absolute redirect (http)
    response = client.post('/login?next=http://evil.com')
    assert response.status_code == 302, "Invalid redirect did not return 302."
    assert response.headers['Location'] == '/home', "Invalid redirect (http) was not redirected to /home."

    # Test invalid absolute redirect (//)
    response = client.post('/login?next=//evil.com')
    assert response.status_code == 302, "Invalid redirect did not return 302."
    assert response.headers['Location'] == '/home', "Invalid redirect (//) was not redirected to /home."

def test_sandbox_exists():
    sandbox_path = "/home/user/sandbox.py"
    assert os.path.isfile(sandbox_path), f"{sandbox_path} is missing."

    with open(sandbox_path, "r") as f:
        content = f.read()

    assert "sys.addaudithook" in content, "sandbox.py does not appear to use sys.addaudithook."
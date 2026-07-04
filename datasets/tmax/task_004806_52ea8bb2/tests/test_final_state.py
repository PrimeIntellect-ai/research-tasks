# test_final_state.py
import os
import json
import requests
import time

def test_admin_key_decrypted():
    key_path = "/home/user/admin_key.pem"
    assert os.path.isfile(key_path), f"{key_path} is missing"
    with open(key_path, "r") as f:
        content = f.read()
    assert "ENCRYPTED" not in content, f"The key at {key_path} is still encrypted"
    assert "PRIVATE KEY" in content, f"The file at {key_path} does not look like a private key"

def test_ssh_audit_json():
    audit_path = "/home/user/ssh_audit.json"
    assert os.path.isfile(audit_path), f"{audit_path} is missing"
    with open(audit_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{audit_path} does not contain valid JSON"

    expected = {"PermitRootLogin": "no", "PasswordAuthentication": "no"}
    assert data == expected, f"Audit JSON content is incorrect. Expected {expected}, got {data}"

def test_service_post_log():
    payload = {"entry": '<script>alert("XSS & Injection")</script>'}
    try:
        r = requests.post("http://127.0.0.1:8080/log", data=payload, timeout=2)
    except requests.RequestException as e:
        assert False, f"Service not reachable or failed on POST /log: {e}"

    assert r.status_code == 200, f"Expected status 200 for POST /log, got {r.status_code}"

    time.sleep(0.5)  # Allow time for the service to flush to disk
    log_path = "/home/user/service_audit.log"
    assert os.path.isfile(log_path), f"Log file {log_path} not created"

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "&lt;script&gt;alert(" in log_content, "Log entry not found or '<' / '>' not properly HTML encoded"
    assert "&quot;XSS &amp; Injection&quot;" in log_content, "Log entry quotes or ampersands not properly HTML encoded"
    assert "&lt;/script&gt;" in log_content, "Log entry closing tags not properly HTML encoded"
    assert "<script>" not in log_content, "Unescaped HTML found in log"

def test_service_get_report_auth():
    headers = {"Authorization": "Bearer ComplianceAdmin7"}
    try:
        r = requests.get("http://127.0.0.1:8080/report", headers=headers, timeout=2)
    except requests.RequestException as e:
        assert False, f"Service not reachable or failed on GET /report: {e}"

    assert r.status_code == 200, f"Expected status 200 for authenticated GET /report, got {r.status_code}"
    try:
        data = r.json()
    except ValueError:
        assert False, "Response to GET /report was not valid JSON"

    expected = {"PermitRootLogin": "no", "PasswordAuthentication": "no"}
    assert data == expected, f"Report endpoint returned incorrect JSON. Expected {expected}, got {data}"

def test_service_get_report_no_auth():
    try:
        r = requests.get("http://127.0.0.1:8080/report", timeout=2)
    except requests.RequestException as e:
        assert False, f"Service not reachable or failed on GET /report: {e}"

    assert r.status_code == 401, f"Expected status 401 for missing auth, got {r.status_code}"

    headers = {"Authorization": "Bearer WrongPass"}
    try:
        r2 = requests.get("http://127.0.0.1:8080/report", headers=headers, timeout=2)
    except requests.RequestException as e:
        assert False, f"Service not reachable or failed on GET /report: {e}"

    assert r2.status_code == 401, f"Expected status 401 for wrong auth, got {r2.status_code}"
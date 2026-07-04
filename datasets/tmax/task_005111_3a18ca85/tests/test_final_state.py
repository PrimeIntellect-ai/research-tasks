# test_final_state.py
import os
import json

def test_audit_report():
    report_path = '/home/user/audit_report.txt'
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 2, "Audit report does not contain enough lines."

    tampered_file_line = content[0].strip()
    cwe_id_line = content[1].strip()

    assert tampered_file_line == "TAMPERED_FILE: /home/user/app/server.js", \
        f"Expected 'TAMPERED_FILE: /home/user/app/server.js', got '{tampered_file_line}'"

    assert cwe_id_line == "CWE_ID: CWE-79", \
        f"Expected 'CWE_ID: CWE-79', got '{cwe_id_line}'"

def test_payload():
    payload_path = '/home/user/payload.txt'
    assert os.path.isfile(payload_path), f"{payload_path} does not exist."

    with open(payload_path, 'r') as f:
        content = f.read().strip()

    valid_payloads = [
        "<script>alert('pwned')</script>",
        "<script>alert(\"pwned\")</script>"
    ]

    assert content in valid_payloads, \
        f"Payload is incorrect. Expected one of {valid_payloads}, got '{content}'"

def test_config_json():
    config_path = '/home/user/app/config.json'
    assert os.path.isfile(config_path), f"{config_path} does not exist."

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{config_path} is not valid JSON."

    assert "Content-Security-Policy" in config, \
        "config.json is missing the 'Content-Security-Policy' key."

    csp_value = config["Content-Security-Policy"].strip()
    assert csp_value == "default-src 'self'", \
        f"Expected CSP value \"default-src 'self'\", got '{csp_value}'"
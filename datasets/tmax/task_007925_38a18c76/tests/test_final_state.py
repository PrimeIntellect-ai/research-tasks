# test_final_state.py

import os
import json
import base64
import pytest

def test_config_json():
    """Verify config.json is generated correctly from legacy_config.b64."""
    config_path = '/home/user/project/config.json'
    assert os.path.isfile(config_path), f"{config_path} is missing. Did build.py run successfully?"

    with open(config_path, 'r') as f:
        try:
            config_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{config_path} does not contain valid JSON.")

    expected_config = {"PORT": "9090", "MODE": "production", "DB": "sqlite"}
    assert config_data == expected_config, f"config.json contents {config_data} do not match expected {expected_config}."

def test_nginx_conf():
    """Verify nginx.conf exists and contains the correct configuration."""
    nginx_conf_path = '/home/user/project/nginx.conf'
    assert os.path.isfile(nginx_conf_path), f"{nginx_conf_path} is missing."

    with open(nginx_conf_path, 'r') as f:
        content = f.read()

    # Check proxy pass
    assert "proxy_pass" in content and "127.0.0.1:9090" in content, \
        "nginx.conf does not contain proxy_pass to http://127.0.0.1:9090"

    # Check header
    assert "add_header" in content and "X-Library-Version" in content and "1.2.9" in content, \
        "nginx.conf does not contain the correct add_header directive for X-Library-Version 1.2.9"

def test_test_report_log():
    """Verify test_report.log contains the correct status, header, and body."""
    report_path = '/home/user/project/test_report.log'
    assert os.path.isfile(report_path), f"{report_path} is missing. Did test_suite.py run successfully?"

    with open(report_path, 'r') as f:
        lines = f.read().strip().splitlines()

    status_line = next((line for line in lines if line.startswith("STATUS:")), None)
    header_line = next((line for line in lines if line.startswith("HEADER:")), None)
    body_line = next((line for line in lines if line.startswith("BODY:")), None)

    assert status_line is not None, "test_report.log is missing the STATUS: line"
    assert header_line is not None, "test_report.log is missing the HEADER: line"
    assert body_line is not None, "test_report.log is missing the BODY: line"

    assert "200" in status_line, f"Expected STATUS to contain 200, got: {status_line}"
    assert "1.2.9" in header_line, f"Expected HEADER to contain 1.2.9, got: {header_line}"

    body_str = body_line.replace("BODY:", "").strip()
    try:
        body_json = json.loads(body_str)
    except json.JSONDecodeError:
        pytest.fail(f"BODY line does not contain valid JSON. Got: {body_str}")

    expected_body = {"PORT": "9090", "MODE": "production", "DB": "sqlite"}
    assert body_json == expected_body, f"Parsed BODY {body_json} does not match expected {expected_body}"
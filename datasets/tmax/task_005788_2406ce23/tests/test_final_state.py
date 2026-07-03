# test_final_state.py
import os
import re
import pytest

def test_nginx_config_fixed():
    conf_path = "/home/user/staging/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "proxy_pass http://unix:/tmp/staging_app.sock;" in content, (
        "Nginx configuration does not contain the correct proxy_pass directive."
    )

def test_logrotate_configured():
    conf_path = "/home/user/staging/logrotate.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read()

    # Check for the correct log file
    assert "/home/user/staging/logs/access.log" in content, (
        "logrotate.conf does not specify the correct log file."
    )

    # Check for required directives
    assert re.search(r'\bdaily\b', content), "logrotate.conf is missing 'daily' directive."
    assert re.search(r'\brotate\s+5\b', content), "logrotate.conf is missing 'rotate 5' directive."
    assert re.search(r'\bcompress\b', content), "logrotate.conf is missing 'compress' directive."

def test_capacity_report_email():
    log_path = "/home/user/staging/logs/access.log"
    assert os.path.isfile(log_path), f"Access log {log_path} does not exist."

    total_bytes = 0
    request_count = 0
    with open(log_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) > 9:
                try:
                    total_bytes += int(parts[9])
                    request_count += 1
                except ValueError:
                    pass

    assert request_count >= 5, f"Expected at least 5 requests in access.log, found {request_count}."

    eml_path = "/home/user/capacity_report.eml"
    assert os.path.isfile(eml_path), f"Email file {eml_path} does not exist."

    with open(eml_path, "r") as f:
        eml_content = f.read()

    assert "To: capacity@example.com" in eml_content, "Email missing correct 'To' header."
    assert "Subject: Staging Capacity Report" in eml_content, "Email missing correct 'Subject' header."

    expected_body = f"Total bytes sent: {total_bytes}"
    assert expected_body in eml_content, (
        f"Email body does not contain the correct sum. Expected '{expected_body}'."
    )
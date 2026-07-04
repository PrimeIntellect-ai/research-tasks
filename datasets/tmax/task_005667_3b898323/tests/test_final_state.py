# test_final_state.py

import os
import json
import pytest

def test_report_file_exists():
    path = "/home/user/reports/report.txt"
    assert os.path.isfile(path), f"Expected report file {path} does not exist. Did the job run successfully and write to the correct directory?"

def test_report_file_content():
    path = "/home/user/reports/report.txt"
    assert os.path.isfile(path), f"Expected report file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "Locale: en_US.UTF-8" in content, "The report file does not contain the correct Locale. Ensure LC_ALL is exported correctly."
    assert "Port: 2525" in content, "The report file does not contain the correct Port. Ensure SMTP_PORT is exported correctly."

    # Check for timezone indicator (PST or PDT for America/Los_Angeles)
    assert "PST" in content or "PDT" in content, "The report file does not contain the correct timezone indicator (PST/PDT). Ensure TZ is exported correctly."

def test_smtp_config_content():
    path = "/home/user/config/smtp.json"
    assert os.path.isfile(path), f"Configuration file {path} does not exist."

    with open(path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected_config = {
        "mailing_list": "active",
        "protocol": "smtp"
    }

    assert config == expected_config, f"The contents of {path} do not exactly match the required JSON structure."

def test_mailer_go_fixed():
    path = "/home/user/app/mailer.go"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # The bug was `repDir := envDir`, it should be `repDir = envDir`
    assert "repDir := envDir" not in content, "The variable shadowing bug in mailer.go has not been fixed."
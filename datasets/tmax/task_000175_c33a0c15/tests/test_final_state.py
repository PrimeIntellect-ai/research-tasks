# test_final_state.py

import os
import configparser
import pytest

def test_deploy_errors_log():
    log_path = "/home/user/deploy_errors.log"
    assert os.path.isfile(log_path), f"Error log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_errors = [
        "ERROR: Service reports_mailer has incomplete network configuration",
        "ERROR: Service legacy_mailer has incomplete network configuration"
    ]

    for err in expected_errors:
        assert err in lines, f"Expected error message not found in {log_path}: '{err}'"

    # Check that there are no extra duplicate errors (idempotency check for log)
    assert len(lines) == 2, f"Expected exactly 2 error lines in {log_path}, found {len(lines)}."

def test_mail_routing_conf():
    conf_path = "/home/user/mail_routing.conf"
    assert os.path.isfile(conf_path), f"Config file {conf_path} is missing."

    config = configparser.ConfigParser()
    try:
        config.read(conf_path)
    except Exception as e:
        pytest.fail(f"Failed to parse {conf_path} as a valid INI file: {e}")

    # Check core_mailer (should be untouched)
    assert "core_mailer" in config.sections(), "[core_mailer] section is missing."
    assert config.get("core_mailer", "target") == "127.0.0.5:2500", "core_mailer target was modified."
    assert config.get("core_mailer", "domain") == "core.internal", "core_mailer domain was modified."

    # Check auth_mailer (should be updated)
    assert "auth_mailer" in config.sections(), "[auth_mailer] section is missing."
    assert config.get("auth_mailer", "target") == "127.0.0.10:2525", "auth_mailer target is incorrect."
    assert config.get("auth_mailer", "domain") == "auth.corp.com", "auth_mailer domain is incorrect."

    # Check billing_mailer (should be added, domain defaulted)
    assert "billing_mailer" in config.sections(), "[billing_mailer] section is missing."
    assert config.get("billing_mailer", "target") == "127.0.0.12:2526", "billing_mailer target is incorrect."
    assert config.get("billing_mailer", "domain") == "billing_mailer.internal", "billing_mailer domain is incorrect."

    # Check that reports_mailer and legacy_mailer are NOT in the config
    assert "reports_mailer" not in config.sections(), "[reports_mailer] should not be in the config."
    assert "legacy_mailer" not in config.sections(), "[legacy_mailer] should not be in the config."

def test_mail_routing_conf_formatting():
    # Ensure exact formatting rules are followed
    conf_path = "/home/user/mail_routing.conf"
    with open(conf_path, "r") as f:
        content = f.read()

    # Check for proper spacing around '=' as specified
    assert "target = 127.0.0.10:2525" in content, "Formatting issue: expected 'target = 127.0.0.10:2525'"
    assert "domain = auth.corp.com" in content, "Formatting issue: expected 'domain = auth.corp.com'"
    assert "target = 127.0.0.12:2526" in content, "Formatting issue: expected 'target = 127.0.0.12:2526'"
    assert "domain = billing_mailer.internal" in content, "Formatting issue: expected 'domain = billing_mailer.internal'"
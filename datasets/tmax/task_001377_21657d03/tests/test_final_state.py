# test_final_state.py

import os
import pytest

def test_expect_script_exists_and_valid():
    expect_script = "/home/user/fix_mail.exp"
    assert os.path.isfile(expect_script), f"Expect script {expect_script} does not exist."

    with open(expect_script, "r") as f:
        content = f.read()

    assert "spawn" in content or "expect" in content, f"Expect script {expect_script} does not appear to contain valid Expect syntax."

def test_mail_config_generated_correctly():
    config_file = "/home/user/mail_config.conf"
    assert os.path.isfile(config_file), f"Configuration file {config_file} was not generated."

    with open(config_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert "ADMIN_EMAIL=sysadmin@company.local" in lines, "Admin email in config file is incorrect or missing."
    assert "SMTP_PORT=2525" in lines, "SMTP port in config file is incorrect or missing."
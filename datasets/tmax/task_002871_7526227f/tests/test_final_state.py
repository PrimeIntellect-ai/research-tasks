# test_final_state.py

import os
import subprocess
import pytest

def test_aliases_config_fixed():
    conf_path = "/home/user/mail_manager/config/aliases.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, 'r') as f:
        lines = f.readlines()

    marketing_fixed = False
    devops_broken = False

    for line in lines:
        if "marketing" in line and "marketing@example.com" in line:
            assert ":" in line, "The 'marketing' line in aliases.conf is still missing a colon."
            marketing_fixed = True
        if "devops devops@example.com missingcolon" in line:
            devops_broken = True

    assert marketing_fixed, "The 'marketing' alias was not found or not fixed properly in aliases.conf."
    assert devops_broken, "The 'devops' alias was modified or removed. It should be left broken."

def test_generate_report_execution_and_output():
    # Remove report.log if it exists to ensure we are testing the script's current behavior
    report_path = "/home/user/mail_manager/report.log"
    if os.path.exists(report_path):
        os.remove(report_path)

    # Run the job script
    script_path = "/home/user/mail_manager/run_job.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_job.sh failed with return code {result.returncode}. Error: {result.stderr}"

    assert os.path.isfile(report_path), "report.log was not generated at the correct absolute path (/home/user/mail_manager/report.log)."

    with open(report_path, 'r') as f:
        report_content = f.read().strip().split('\n')

    expected_lines = [
        "admin -> admin@example.com",
        "support -> support@example.com",
        "marketing -> marketing@example.com",
        "ERROR: Malformed line - devops devops@example.com missingcolon"
    ]

    for expected in expected_lines:
        assert expected in report_content, f"Expected line '{expected}' not found in report.log."

    assert len(report_content) == len(expected_lines), f"report.log contains an unexpected number of lines. Expected {len(expected_lines)}, got {len(report_content)}."
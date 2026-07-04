# test_final_state.py

import os
import pytest

def test_safe_files_extracted():
    db_conf_path = "/home/user/safe_configs/service/db.conf"
    app_conf_path = "/home/user/safe_configs/service/app.conf"

    assert os.path.exists(db_conf_path), f"Safe file {db_conf_path} was not extracted."
    assert os.path.exists(app_conf_path), f"Safe file {app_conf_path} was not extracted."

    with open(db_conf_path, "r") as f:
        assert f.read() == "db=prod", f"Content of {db_conf_path} is incorrect."

    with open(app_conf_path, "r") as f:
        assert f.read() == "port=8080", f"Content of {app_conf_path} is incorrect."

def test_malicious_files_not_extracted():
    evil_sh_path = "/home/user/evil.sh"
    fake_shadow_path = "/etc/fake_shadow"

    assert not os.path.exists(evil_sh_path), f"Malicious file {evil_sh_path} was extracted!"
    assert not os.path.exists(fake_shadow_path), f"Malicious file {fake_shadow_path} was extracted!"

def test_report_content():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."

    expected_content = "Filename: db.conf\nContent: db=prod"

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Report content is incorrect. Expected:\n{expected_content}\nGot:\n{content}"
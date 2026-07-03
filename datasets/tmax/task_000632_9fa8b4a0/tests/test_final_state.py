# test_final_state.py

import os
import json
import pytest

def test_config_json_fixed():
    path = "/home/user/service/config.json"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} does not contain valid JSON.")

    assert "port" in config, f"'port' key missing in {path}."
    assert config["port"] == 8080, f"Expected port to be 8080, got {config['port']}."

def test_expect_script_exists():
    path = "/home/user/start_service.exp"
    assert os.path.isfile(path), f"Expect script {path} does not exist."

def test_logrotate_conf():
    path = "/home/user/logrotate.conf"
    assert os.path.isfile(path), f"Logrotate config {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "/home/user/service/daemon.log" in content, f"Logrotate config does not target /home/user/service/daemon.log."
    assert "daily" in content, f"Logrotate config missing 'daily' directive."
    assert "rotate 3" in content, f"Logrotate config missing 'rotate 3' directive."
    assert "create" in content, f"Logrotate config missing 'create' directive."

def test_daemon_log_success():
    path = "/home/user/service/daemon.log"
    assert os.path.isfile(path), f"Log file {path} does not exist. Did the service run successfully?"
    with open(path, "r") as f:
        content = f.read()

    expected_msg = "Service started successfully on port 8080"
    assert expected_msg in content, f"Expected success message not found in {path}."
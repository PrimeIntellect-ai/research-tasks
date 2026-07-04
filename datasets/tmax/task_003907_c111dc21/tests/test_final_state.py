# test_final_state.py

import os
import json
import subprocess
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_script():
    script_path = "/home/user/restore_tester.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_extracted_files():
    assert os.path.isdir("/home/user/restore_test"), "/home/user/restore_test/ directory does not exist."
    assert os.path.exists("/home/user/restore_test/deploy_pipeline.log"), "deploy_pipeline.log was not extracted to /home/user/restore_test/."
    assert os.path.exists("/home/user/restore_test/proxy_template.conf"), "proxy_template.conf was not extracted to /home/user/restore_test/."

def test_local_proxy_conf():
    conf_path = "/home/user/restore_test/local_proxy.conf"
    assert os.path.exists(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "listen 8080;" in content, "listen 8080; not found in local_proxy.conf"
    assert "listen 8443;" in content, "listen 8443; not found in local_proxy.conf"
    assert "listen 80;" not in content, "listen 80; should have been replaced."
    assert "listen 443;" not in content, "listen 443; should have been replaced."

def test_restore_report_json():
    report_path = "/home/user/restore_report.json"
    assert os.path.exists(report_path), f"{report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON.")

    assert "last_successful_deploy_tokyo" in data, "Missing key 'last_successful_deploy_tokyo' in JSON."
    assert data["last_successful_deploy_tokyo"] == "2023-10-05 01:30:00", f"Incorrect timestamp: {data['last_successful_deploy_tokyo']}"

    assert "proxy_listen_ports" in data, "Missing key 'proxy_listen_ports' in JSON."
    assert isinstance(data["proxy_listen_ports"], list), "'proxy_listen_ports' must be a JSON array."

    ports = set(str(p) for p in data["proxy_listen_ports"])
    assert ports == {"8080", "8443"}, f"Incorrect ports in JSON: {data['proxy_listen_ports']}"
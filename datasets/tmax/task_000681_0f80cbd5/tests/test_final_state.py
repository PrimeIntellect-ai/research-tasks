# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_nginx_config_fixed():
    nginx_conf = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf), f"Nginx configuration file {nginx_conf} does not exist."
    with open(nginx_conf, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:8000;" in content, (
        "Nginx configuration was not updated correctly. "
        "Expected 'proxy_pass http://127.0.0.1:8000;' to be present."
    )

def test_symlink_created():
    symlink_path = "/home/user/app/data"
    expected_target = "/home/user/source_data"

    assert os.path.islink(symlink_path), f"Path {symlink_path} is not a symlink. The deployment script failed to create it."

    actual_target = os.readlink(symlink_path)
    assert actual_target == expected_target, (
        f"Symlink {symlink_path} points to {actual_target}, "
        f"but expected it to point to {expected_target}."
    )

def test_verification_log():
    log_file = "/home/user/verification.log"
    assert os.path.isfile(log_file), f"Verification log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read().strip()

    expected_content = "production_secret_data_7741"
    assert content == expected_content, (
        f"Verification log content is incorrect. "
        f"Expected '{expected_content}', got '{content}'."
    )

def test_deploy_script_exists():
    deploy_script = "/home/user/deploy.py"
    assert os.path.isfile(deploy_script), f"Deployment script {deploy_script} does not exist."

def test_live_endpoint():
    url = "http://127.0.0.1:8080/data"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8').strip()

        expected_content = "production_secret_data_7741"
        assert content == expected_content, (
            f"Live endpoint returned incorrect data. "
            f"Expected '{expected_content}', got '{content}'."
        )
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx or application via {url}. Error: {e}")
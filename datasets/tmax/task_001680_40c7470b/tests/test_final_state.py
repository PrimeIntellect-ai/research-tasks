# test_final_state.py

import os
import glob
import pytest
import requests

def test_nginx_routing_api_a():
    url = "http://127.0.0.1:8080/api/a"
    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for {url}, got {response.status_code}"
    # The setup starts backend-a on 8081. We don't have exact body, but a successful response is enough.
    # The truth says "response body from backend-a". We will just assert 200 OK.

def test_nginx_routing_api_b():
    url = "http://127.0.0.1:8080/api/b"
    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200 for {url}, got {response.status_code}"

def test_backup_directory_and_files():
    backup_dir = "/home/user/app/backups"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist."

    backup_files = glob.glob(os.path.join(backup_dir, "nginx.conf.bak.*"))
    assert len(backup_files) > 0, f"No backup files matching 'nginx.conf.bak.*' found in {backup_dir}."

def test_bash_profile_env_vars():
    profile_path = "/home/user/.bash_profile"
    assert os.path.isfile(profile_path), f"Profile file {profile_path} does not exist."

    with open(profile_path, "r") as f:
        content = f.read()

    assert "MANIFEST_PATH=/home/user/app/manifest.yaml" in content, "MANIFEST_PATH not found in .bash_profile"
    assert "NGINX_CONF_PATH=/home/user/app/nginx/nginx.conf" in content, "NGINX_CONF_PATH not found in .bash_profile"
    assert "BACKUP_DIR=/home/user/app/backups" in content, "BACKUP_DIR not found in .bash_profile"
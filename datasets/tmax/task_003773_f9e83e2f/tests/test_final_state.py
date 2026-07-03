# test_final_state.py

import os
import tarfile
import requests
import pytest
import urllib3

# Suppress insecure request warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_backup_tarball():
    tar_path = "/home/user/config_backup.tar.gz"
    assert os.path.isfile(tar_path), f"Backup archive {tar_path} does not exist."

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            names = tar.getnames()
            # The tarball should contain the contents of config_template
            # It might include the directory itself or just the files
            assert any("bashttpd.conf" in name for name in names), "bashttpd.conf not found in the backup tarball."
    except tarfile.ReadError:
        pytest.fail(f"File {tar_path} is not a valid gzip-compressed tar archive.")

def test_bashttpd_conf():
    conf_path = "/home/user/bashttpd.conf"
    assert os.path.isfile(conf_path), f"Configuration file {conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/www" in content, f"The configuration file {conf_path} does not seem to point to /home/user/www."

def test_cert_and_key_exist():
    cert_path = "/home/user/cert.pem"
    key_path = "/home/user/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Private key file {key_path} does not exist."

def test_expect_script_exists():
    script_path = "/home/user/start_service.exp"
    assert os.path.isfile(script_path), f"Expect script {script_path} does not exist."

def test_https_service():
    url = "https://127.0.0.1:8443/index.html"
    index_path = "/home/user/www/index.html"

    assert os.path.isfile(index_path), f"Index file {index_path} does not exist."
    with open(index_path, "r") as f:
        expected_content = f.read().strip()

    try:
        response = requests.get(url, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTPS service at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP status 200, but got {response.status_code}."
    assert expected_content in response.text, "The content returned by the web server does not match the expected index.html content."
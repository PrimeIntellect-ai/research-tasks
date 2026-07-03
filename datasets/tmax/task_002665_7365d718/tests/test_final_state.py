# test_final_state.py

import os
import tarfile
import urllib.request
import ssl
import pytest

def test_backup_tarball_exists_and_valid():
    backup_path = "/home/user/backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # Check if main.json is in the tarball (ignoring leading paths)
            assert any(name.endswith("main.json") for name in names), \
                f"Backup tarball {backup_path} does not contain 'main.json'."
    except tarfile.TarError:
        pytest.fail(f"File {backup_path} is not a valid gzip-compressed tarball.")

def test_tls_certificates_exist():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Private key file {key_path} does not exist."

def test_https_server_serving_metrics():
    url = "https://localhost:8443/data.txt"

    # Create an unverified SSL context to bypass self-signed cert validation
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP status 200, got {response.status}"
            content = response.read().decode('utf-8')
            assert "cpu_usage_percent 45.2" in content, \
                f"Expected 'cpu_usage_percent 45.2' in response, got: {content}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the HTTPS server at {url}. Is the server running? Error: {e}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred while testing the HTTPS server: {e}")
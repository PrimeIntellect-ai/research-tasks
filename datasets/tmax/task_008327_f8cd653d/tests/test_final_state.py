# test_final_state.py

import os
import subprocess

def test_service_file_fixed():
    service_path = "/home/user/.config/systemd/user/secure-app.service"
    assert os.path.isfile(service_path), f"Service file {service_path} is missing."

    with open(service_path, "r") as f:
        content = f.read()

    assert "LimitFSIZE" not in content, "LimitFSIZE directive was not removed from the service file."

def test_tls_certificates_exist():
    cert_path = "/home/user/app/cert.pem"
    key_path = "/home/user/app/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Private key file {key_path} is missing."

def test_service_is_active():
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "secure-app.service"],
            capture_output=True,
            text=True,
            check=False
        )
        assert result.stdout.strip() == "active", f"Service is not active. Output: {result.stdout.strip()}"
    except FileNotFoundError:
        assert False, "systemctl command not found."

def test_success_file_contains_200():
    success_path = "/home/user/success.txt"
    assert os.path.isfile(success_path), f"File {success_path} is missing."

    with open(success_path, "r") as f:
        content = f.read().strip()

    assert content == "200", f"Expected success.txt to contain '200', but found '{content}'."
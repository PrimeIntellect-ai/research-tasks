# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_bash_profile_env_vars():
    profile_path = "/home/user/.bash_profile"
    assert os.path.isfile(profile_path), f"{profile_path} does not exist."

    with open(profile_path, "r") as f:
        content = f.read()

    assert "APP_PORT=8443" in content, "APP_PORT=8443 missing in .bash_profile"
    assert "APP_LOG_DIR=/home/user/app_logs" in content, "APP_LOG_DIR=/home/user/app_logs missing in .bash_profile"
    assert "TLS_DIR=/home/user/tls" in content, "TLS_DIR=/home/user/tls missing in .bash_profile"

def test_tls_certificates_exist_and_valid():
    crt_path = "/home/user/tls/server.crt"
    key_path = "/home/user/tls/server.key"

    assert os.path.isfile(crt_path), f"Certificate {crt_path} does not exist."
    assert os.path.isfile(key_path), f"Key {key_path} does not exist."

    # Check subject using openssl
    result = subprocess.run(
        ["openssl", "x509", "-in", crt_path, "-noout", "-subject"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to read certificate with openssl."

    # The output format can vary slightly depending on openssl version, but should contain the components
    subject = result.stdout
    assert "C = US" in subject or "C=US" in subject, "Country (C) not found or incorrect in cert subject."
    assert "ST = State" in subject or "ST=State" in subject, "State (ST) not found or incorrect in cert subject."
    assert "L = City" in subject or "L=City" in subject, "Locality (L) not found or incorrect in cert subject."
    assert "O = Company" in subject or "O=Company" in subject, "Organization (O) not found or incorrect in cert subject."
    assert "CN = localhost" in subject or "CN=localhost" in subject, "Common Name (CN) not found or incorrect in cert subject."

def test_log_rotation_artifacts():
    log_bak_gz = "/home/user/app_logs/server.log.bak.gz"
    assert os.path.isfile(log_bak_gz), f"Rotated log archive {log_bak_gz} does not exist. Did you run deploy.sh twice as instructed?"

def test_current_log_file():
    log_file = "/home/user/app_logs/server.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    expected_line = "Starting server on port 8443 with cert /home/user/tls/server.crt"
    assert expected_line in content, f"Log file does not contain the expected startup message. Found: {content}"

def test_scripts_are_executable():
    scripts = [
        "/home/user/setup_tls.sh",
        "/home/user/rotate.sh",
        "/home/user/deploy.sh"
    ]

    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        st = os.stat(script)
        assert bool(st.st_mode & stat.S_IXUSR), f"Script {script} is not executable."
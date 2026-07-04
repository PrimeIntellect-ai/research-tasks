# test_final_state.py
import os
import urllib.request
import ssl
import subprocess
import json

def test_archive_web_directory_and_files():
    archive_dir = "/home/user/archive_web"
    assert os.path.isdir(archive_dir), f"Directory {archive_dir} does not exist."

    expected_files = {
        "report_20230110_160000_UTC.dat": "Winter data\n",
        "report_20230715_213000_UTC.dat": "Summer data\n"
    }

    for filename, content in expected_files.items():
        filepath = os.path.join(archive_dir, filename)
        assert os.path.isfile(filepath), f"Expected file {filename} not found in {archive_dir}. Timezone conversion might be incorrect."
        with open(filepath, "r") as f:
            assert f.read() == content, f"Content of {filename} does not match expected data."

def test_tls_certificate_and_key():
    cert_path = "/home/user/tls.crt"
    key_path = "/home/user/tls.key"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Key file {key_path} does not exist."

    # Check certificate subject
    try:
        subject_output = subprocess.check_output(
            ["openssl", "x509", "-in", cert_path, "-noout", "-subject"],
            text=True
        )
        assert "CN = migration.local" in subject_output, f"Certificate Common Name is incorrect: {subject_output}"
    except subprocess.CalledProcessError:
        assert False, "Failed to read certificate subject using openssl."

def test_server_pid():
    pid_file = "/home/user/server.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file does not contain a valid integer: {pid_str}"
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running."

def test_https_web_server():
    # Create an unverified SSL context to allow self-signed certificates
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    expected_files = {
        "report_20230110_160000_UTC.dat": b"Winter data\n",
        "report_20230715_213000_UTC.dat": b"Summer data\n"
    }

    for filename, expected_content in expected_files.items():
        url = f"https://localhost:8443/{filename}"
        try:
            with urllib.request.urlopen(url, context=ctx, timeout=5) as response:
                assert response.status == 200, f"Failed to fetch {filename}, HTTP status {response.status}"
                content = response.read()
                assert content == expected_content, f"Served content for {filename} does not match expected data."
        except urllib.error.URLError as e:
            assert False, f"Failed to connect to HTTPS server on port 8443 or fetch {filename}: {e}"
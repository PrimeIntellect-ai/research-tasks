# test_final_state.py
import os
import subprocess
import socket
import ssl
import time
import requests
from pathlib import Path
import urllib3

# Disable insecure request warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_manifests_directory_and_acls():
    manifests_dir = Path("/home/user/manifests")
    assert manifests_dir.is_dir(), f"Directory {manifests_dir} does not exist."

    # Check ACLs using getfacl
    result = subprocess.run(['getfacl', '-c', str(manifests_dir)], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run getfacl."

    output = result.stdout.strip()
    assert "user::rwx" in output, "ACL missing user::rwx"
    assert "group::---" in output, "ACL missing group::---"
    assert "other::---" in output, "ACL missing other::---"

def test_nginx_manifest_file():
    manifest_file = Path("/home/user/manifests/nginx.yaml")
    assert manifest_file.is_file(), f"Manifest file {manifest_file} does not exist."

    content = manifest_file.read_text()
    assert "kind: Deployment" in content, "Manifest does not contain 'kind: Deployment'"
    assert "nginx:latest" in content, "Manifest does not contain 'nginx:latest'"
    assert "replicas: 2" in content or "replicas:2" in content, "Manifest does not contain 2 replicas"

def test_fstab_configuration():
    fstab_file = Path("/home/user/operator.fstab")
    assert fstab_file.is_file(), f"File {fstab_file} does not exist."

    content = fstab_file.read_text()
    found = False
    for line in content.splitlines():
        parts = line.split()
        if len(parts) >= 4 and parts[0] == "/dev/sdb1" and parts[1] == "/home/user/manifests" and parts[2] == "ext4":
            opts = parts[3].split(',')
            if set(["noexec", "nosuid", "nodev"]).issubset(set(opts)):
                found = True
                break
    assert found, "Valid fstab entry for /dev/sdb1 to /home/user/manifests not found in /home/user/operator.fstab"

def test_tls_certificates():
    crt_file = Path("/home/user/certs/server.crt")
    key_file = Path("/home/user/certs/server.key")

    assert crt_file.is_file(), f"Certificate file {crt_file} does not exist."
    assert key_file.is_file(), f"Private key file {key_file} does not exist."

def test_https_server_valid_token():
    url = "https://127.0.0.1:8443/api/v1/manifest"
    headers = {"Authorization": "Bearer op-secret-14"}

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to HTTPS server: {e}"

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    body = response.text
    assert "kind: Deployment" in body, "Response body missing 'kind: Deployment'"
    assert "nginx:latest" in body, "Response body missing 'nginx:latest'"

def test_https_server_invalid_token():
    url = "https://127.0.0.1:8443/api/v1/manifest"
    headers = {"Authorization": "Bearer op-secret-99"}

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to HTTPS server: {e}"

    assert response.status_code == 403, f"Expected HTTP 403 for invalid token, got {response.status_code}"
    assert not response.text.strip(), "Expected empty body for HTTP 403"

def test_tcp_trap():
    host = "127.0.0.1"
    port = 8022

    try:
        s = socket.create_connection((host, port), timeout=5)
    except socket.error as e:
        assert False, f"Failed to connect to TCP trap on {host}:{port}: {e}"

    try:
        # Send some data
        s.sendall(b"SSH-2.0-OpenSSH_8.4p1\r\n")

        # Wait for connection to be closed
        data = s.recv(1024)
        assert len(data) == 0, f"Expected connection to be closed silently, but received data: {data}"
    except ConnectionResetError:
        # This is also an acceptable way to close the connection
        pass
    except socket.error as e:
        assert False, f"Socket error while communicating with TCP trap: {e}"
    finally:
        s.close()
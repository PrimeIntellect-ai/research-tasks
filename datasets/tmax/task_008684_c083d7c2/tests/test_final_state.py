# test_final_state.py

import os
import json
import subprocess
import pytest

def test_qcow2_images():
    base_path = "/home/user/backup/base.qcow2"
    snap_path = "/home/user/backup/snapshot.qcow2"

    assert os.path.isfile(base_path), f"Base image not found at {base_path}"
    assert os.path.isfile(snap_path), f"Snapshot image not found at {snap_path}"

    # Check base image size
    result = subprocess.run(["qemu-img", "info", "--output=json", base_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run qemu-img on {base_path}"
    base_info = json.loads(result.stdout)
    assert base_info.get("virtual-size") == 50 * 1024 * 1024, f"Base image size is not 50M"
    assert base_info.get("format") == "qcow2", f"Base image format is not qcow2"

    # Check snapshot backing file
    result = subprocess.run(["qemu-img", "info", "--output=json", snap_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run qemu-img on {snap_path}"
    snap_info = json.loads(result.stdout)
    backing_file = snap_info.get("backing-filename")
    assert backing_file is not None, f"Snapshot image does not have a backing file"
    assert "base.qcow2" in backing_file, f"Snapshot backing file is not base.qcow2 (got {backing_file})"
    assert snap_info.get("format") == "qcow2", f"Snapshot image format is not qcow2"

def test_tls_certificates():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"

    assert os.path.isfile(cert_path), f"Certificate not found at {cert_path}"
    assert os.path.isfile(key_path), f"Private key not found at {key_path}"

    # Check certificate CN
    result = subprocess.run(["openssl", "x509", "-in", cert_path, "-noout", "-subject"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read certificate subject"
    assert "CN = localhost" in result.stdout or "CN=localhost" in result.stdout, "Certificate Common Name (CN) is not localhost"

    # Check key is RSA
    result = subprocess.run(["openssl", "rsa", "-in", key_path, "-check", "-noout"], capture_output=True, text=True)
    assert result.returncode == 0, "Private key is invalid or not an unencrypted RSA key"

def test_port_manager_executable():
    bin_path = "/home/user/bin/port_manager"
    assert os.path.isfile(bin_path), f"Compiled binary not found at {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Binary at {bin_path} is not executable"

    with open(bin_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"File at {bin_path} is not an ELF executable"

def test_start_proxy_script():
    script_path = "/home/user/start_proxy.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

    with open(script_path, "r") as f:
        content = f.read().strip()

    expected = "socat openssl-listen:8443,reuseaddr,fork,cert=/home/user/certs/cert.pem,key=/home/user/certs/key.pem,verify=0 tcp:127.0.0.1:9090"
    assert content == expected, f"Script content is incorrect. Expected: {expected}, Got: {content}"
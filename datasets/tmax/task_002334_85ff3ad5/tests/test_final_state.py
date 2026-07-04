# test_final_state.py
import os
import hashlib
import json

def test_incoming_directory_empty():
    """Test that the incoming directory is empty (files were processed and deleted)."""
    incoming_dir = "/home/user/incoming"
    assert os.path.exists(incoming_dir), f"Directory {incoming_dir} should exist."
    files = os.listdir(incoming_dir)
    assert len(files) == 0, f"Incoming directory is not empty. Found: {files}"

def test_app_conf_deployed():
    """Test that app.conf was successfully deployed with the correct content."""
    app_conf_path = "/home/user/configs/app.conf"
    assert os.path.exists(app_conf_path), f"File {app_conf_path} was not deployed."

    with open(app_conf_path, "r") as f:
        content = f.read()

    expected_content = "port=8080\nenable_feature=true\n"
    assert content == expected_content, f"Content of {app_conf_path} is incorrect."

def test_zip_slip_prevented():
    """Test that the malicious file was not extracted/deployed."""
    hacked_txt_path = "/home/user/configs/hacked.txt"
    assert not os.path.exists(hacked_txt_path), f"Malicious file {hacked_txt_path} was deployed! Zip Slip prevention failed."

def test_security_log():
    """Test that the security log correctly recorded the rejected file."""
    log_path = "/home/user/configs/security.log"
    assert os.path.exists(log_path), f"Security log {log_path} does not exist."

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_log_entry = "REJECTED: bundle2.tar.gz - ../../../home/user/configs/hacked.txt"
    assert expected_log_entry in log_content, f"Security log does not contain the expected rejection entry. Found: {log_content}"

def test_manifest_generated():
    """Test that the manifest.txt was generated correctly with the right SHA-256 hash."""
    manifest_path = "/home/user/configs/manifest.txt"
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} does not exist."

    # Calculate expected hash
    expected_content = b"port=8080\nenable_feature=true\n"
    expected_hash = hashlib.sha256(expected_content).hexdigest()
    expected_line = f"{expected_hash}  app.conf"

    with open(manifest_path, "r") as f:
        manifest_content = f.read()

    assert expected_line in manifest_content, f"Manifest does not contain the expected entry for app.conf. Found: {manifest_content}"
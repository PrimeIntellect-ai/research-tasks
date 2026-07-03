# test_final_state.py

import os
import json
import hashlib
import pytest

def test_zip_slip_prevented():
    """Verify that the zip slip payload was not extracted."""
    pwned_path = '/home/user/pwned.txt'
    assert not os.path.exists(pwned_path), f"Security failure: {pwned_path} was extracted! Zip slip vulnerability detected."

def test_extracted_files_content_and_encoding():
    """Verify that the files were extracted and converted to UTF-8 correctly."""
    server_conf_path = '/home/user/config_target/server.conf'
    settings_txt_path = '/home/user/config_target/app/settings.txt'

    assert os.path.exists(server_conf_path), f"File missing: {server_conf_path}"
    assert os.path.exists(settings_txt_path), f"File missing: {settings_txt_path}"

    with open(server_conf_path, 'rb') as f:
        server_conf_content = f.read()

    with open(settings_txt_path, 'rb') as f:
        settings_txt_content = f.read()

    expected_server_conf = "port=8080\nnaïve=true".encode('utf-8')
    expected_settings_txt = "café=open\n".encode('utf-8')

    assert server_conf_content == expected_server_conf, f"Content mismatch or encoding error in {server_conf_path}"
    assert settings_txt_content == expected_settings_txt, f"Content mismatch or encoding error in {settings_txt_path}"

def test_manifest_json():
    """Verify that the manifest.json is generated correctly with proper SHA-256 hashes."""
    manifest_path = '/home/user/manifest.json'
    assert os.path.exists(manifest_path), f"Manifest file missing: {manifest_path}"

    with open(manifest_path, 'r', encoding='utf-8') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {manifest_path} is not valid JSON.")

    expected_server_conf_hash = hashlib.sha256("port=8080\nnaïve=true".encode('utf-8')).hexdigest()
    expected_settings_txt_hash = hashlib.sha256("café=open\n".encode('utf-8')).hexdigest()

    expected_manifest = {
        "server.conf": expected_server_conf_hash,
        "app/settings.txt": expected_settings_txt_hash
    }

    assert manifest == expected_manifest, f"Manifest contents do not match expected values. Got: {manifest}"
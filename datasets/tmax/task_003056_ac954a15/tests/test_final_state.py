# test_final_state.py
import os
import json
import hashlib
import pytest

def test_manifest_json():
    manifest_path = "/home/user/manifest.json"
    assert os.path.exists(manifest_path), f"Manifest file missing: {manifest_path}"

    with open(manifest_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file is not valid JSON: {manifest_path}")

    # Compute expected hashes
    content1 = b"server { listen 80; }"
    content3 = b'{"key": "value"}'

    hash1 = hashlib.sha256(content1).hexdigest()
    hash3 = hashlib.sha256(content3).hexdigest()

    expected_manifest = {
        "/home/user/extracted/nginx/valid1.conf": hash1,
        "/home/user/extracted/app/valid3.json": hash3
    }

    assert isinstance(manifest, dict), "Manifest should be a JSON dictionary."
    assert len(manifest) == len(expected_manifest), f"Manifest should contain exactly {len(expected_manifest)} entries."

    for key, expected_hash in expected_manifest.items():
        assert key in manifest, f"Missing expected file path in manifest: {key}"
        assert manifest[key] == expected_hash, f"Incorrect hash for {key}. Expected {expected_hash}, got {manifest[key]}"

def test_security_alerts_log():
    log_path = "/home/user/security_alerts.log"
    assert os.path.exists(log_path), f"Security alerts log missing: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_alerts = {
        "ALERT: Path traversal detected - /etc/cron.d/mal1.sh",
        "ALERT: Path traversal detected - ../ssh/mal2.conf",
        "ALERT: Path traversal detected - nginx/../../mal3.xml"
    }

    actual_alerts = set(lines)

    missing = expected_alerts - actual_alerts
    extra = actual_alerts - expected_alerts

    assert not missing, f"Missing expected security alerts: {missing}"
    assert not extra, f"Unexpected security alerts found: {extra}"
    assert len(lines) == len(expected_alerts), "Log contains duplicate or extra lines not accounted for."
# test_final_state.py

import os
import json
import hashlib
import pytest

def get_sha256(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def test_manifest_json():
    manifest_path = "/home/user/manifest.json"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    with open(manifest_path, "r") as f:
        try:
            manifest_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {manifest_path} is not valid JSON.")

    expected_manifest = {
        "app.conf": get_sha256("port=8080"),
        "db.conf": get_sha256("host=localhost"),
        "nginx.conf": get_sha256("worker_processes 1;")
    }

    assert manifest_data == expected_manifest, (
        f"Manifest data is incorrect. Expected {expected_manifest}, but got {manifest_data}."
    )

def test_modified_log():
    log_path = "/home/user/modified.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["db.conf", "new.conf"]

    assert lines == expected_lines, (
        f"Modified log is incorrect. Expected {expected_lines}, but got {lines}. "
        "Ensure the output is sorted alphabetically and contains only modified or new files."
    )
# test_final_state.py

import os
import json
import tarfile
import pytest
import requests

BASE_URL = "http://127.0.0.1:9090"
DATA_DIR = "/app/data"
WAL_FILE = os.path.join(DATA_DIR, "config.wal")
SNAPSHOT_FILE = os.path.join(DATA_DIR, "snapshot.json")
SYMLINK_FILE = os.path.join(DATA_DIR, "current.tar.gz")

def test_server_and_state():
    # 1. Send /append requests
    payloads = [
        b'{"key": "app_name", "value": "t\xe9st_app"}',
        b'{"key": "version", "value": "1.0"}',
        b'{"key": "version", "value": "1.1"}'
    ]

    for i, payload in enumerate(payloads):
        try:
            response = requests.post(f"{BASE_URL}/append", data=payload, timeout=5)
            assert response.status_code == 200, f"POST /append request {i+1} failed with status {response.status_code}. Response: {response.text}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to server for POST /append: {e}")

    # 2. Send /commit request
    try:
        response = requests.post(f"{BASE_URL}/commit", timeout=5)
        assert response.status_code == 200, f"POST /commit failed with status {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server for POST /commit: {e}")

    # 3. Verify directory exists
    assert os.path.isdir(DATA_DIR), f"Directory {DATA_DIR} does not exist."

    # 4. Verify WAL file is empty
    assert os.path.isfile(WAL_FILE), f"WAL file {WAL_FILE} does not exist."
    assert os.path.getsize(WAL_FILE) == 0, f"WAL file {WAL_FILE} is not empty."

    # 5. Verify snapshot.json
    assert os.path.isfile(SNAPSHOT_FILE), f"Snapshot file {SNAPSHOT_FILE} does not exist."
    with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
        try:
            snapshot_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {SNAPSHOT_FILE} does not contain valid JSON.")

    expected_data = {"app_name": "tést_app", "version": "1.1"}
    assert snapshot_data == expected_data, f"Snapshot data mismatch. Expected {expected_data}, got {snapshot_data}."

    # 6. Verify symlink
    assert os.path.islink(SYMLINK_FILE), f"{SYMLINK_FILE} is not a symbolic link."
    target = os.readlink(SYMLINK_FILE)
    target_path = os.path.join(DATA_DIR, target) if not os.path.isabs(target) else target
    assert os.path.isfile(target_path), f"Symlink target {target_path} does not exist."
    assert target_path.endswith(".tar.gz"), f"Symlink target {target_path} does not end with .tar.gz."

    # 7. Verify tarball contents
    try:
        with tarfile.open(target_path, "r:gz") as tar:
            members = tar.getnames()
            assert "snapshot.json" in members, f"snapshot.json not found in tarball {target_path}."
            assert len(members) == 1, f"Tarball contains unexpected files: {members}"

            f = tar.extractfile("snapshot.json")
            assert f is not None, "Could not extract snapshot.json from tarball."
            tar_data = json.loads(f.read().decode("utf-8"))
            assert tar_data == expected_data, f"Tarball snapshot data mismatch. Expected {expected_data}, got {tar_data}."
    except tarfile.TarError as e:
        pytest.fail(f"Failed to read tarball {target_path}: {e}")
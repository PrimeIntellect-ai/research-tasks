# test_final_state.py

import os
import tarfile
import json
import threading
import requests
import pytest

ZONE_ID = "STORAGE-77X"
BASE_URL = "http://127.0.0.1:8888"

def test_renamed_files():
    expected_processed = [
        f"/app/logs/processed_{ZONE_ID}_001.log",
        f"/app/logs/processed_{ZONE_ID}_002.log",
        f"/app/logs/processed_{ZONE_ID}_003.log"
    ]
    for f in expected_processed:
        assert os.path.isfile(f), f"Expected processed file {f} is missing."

    unexpected_raw = [
        f"/app/logs/raw_{ZONE_ID}_001.log",
        f"/app/logs/raw_{ZONE_ID}_002.log",
        f"/app/logs/raw_{ZONE_ID}_003.log"
    ]
    for f in unexpected_raw:
        assert not os.path.exists(f), f"Raw file {f} should have been renamed."

def test_untouched_files():
    untouched = "/app/logs/raw_OTHER-11A_001.log"
    assert os.path.isfile(untouched), f"File {untouched} should remain untouched."

def test_archive_exists_and_valid():
    archive_path = f"/app/archive_{ZONE_ID}.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} is missing."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()
        # Check that the 3 processed files are in the archive
        basenames = [os.path.basename(name) for name in names]
        for i in range(1, 4):
            expected_name = f"processed_{ZONE_ID}_00{i}.log"
            assert expected_name in basenames, f"Archive is missing {expected_name}"

def test_server_info_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/info", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {BASE_URL}/info: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()
    assert data.get("zone") == ZONE_ID, f"Expected zone {ZONE_ID}, got {data.get('zone')}"
    assert data.get("files_archived") == 3, f"Expected files_archived 3, got {data.get('files_archived')}"

def test_server_register_concurrency():
    errors = []

    def post_register(i):
        try:
            payload = {"filename": f"test_{i}.log"}
            res = requests.post(f"{BASE_URL}/register", json=payload, timeout=5)
            if res.status_code not in (200, 201, 204):
                errors.append(f"Request {i} failed with status {res.status_code}")
        except Exception as e:
            errors.append(f"Request {i} exception: {e}")

    threads = []
    for i in range(10):
        t = threading.Thread(target=post_register, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert not errors, f"Errors occurred during concurrent POST requests: {errors}"

    registry_path = "/app/registry.json"
    assert os.path.isfile(registry_path), f"Registry file {registry_path} is missing."

    with open(registry_path, "r") as f:
        try:
            registry = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("registry.json is not valid JSON.")

    assert isinstance(registry, list), "registry.json should contain a JSON array."

    expected_filenames = {f"test_{i}.log" for i in range(10)}
    actual_filenames = set(registry)

    missing = expected_filenames - actual_filenames
    assert not missing, f"Missing filenames in registry due to concurrency issues: {missing}"
    assert len(registry) >= 10, f"Registry contains fewer entries than expected. Length: {len(registry)}"
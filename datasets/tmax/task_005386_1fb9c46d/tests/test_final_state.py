# test_final_state.py

import os
import json
import csv
import hashlib
import subprocess
import requests

def get_file_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_archive_files_exist_and_redacted():
    archive_dir = "/app/data/archive"
    assert os.path.isdir(archive_dir), f"Archive directory {archive_dir} does not exist."

    file1_path = os.path.join(archive_dir, "file1.json")
    assert os.path.isfile(file1_path), "file1.json is missing from the archive."
    with open(file1_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "file1.json in archive is not valid JSON."
        assert data.get("email") == "[REDACTED]", "Email in file1.json was not correctly redacted."
        assert "CONFIDENTIAL" in str(data), "Original CONFIDENTIAL data was lost in file1.json."

    file2_path = os.path.join(archive_dir, "file2.csv")
    assert os.path.isfile(file2_path), "file2.csv is missing from the archive."
    with open(file2_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert len(rows) > 0, "file2.csv is empty."
        assert rows[0][1] == "[REDACTED]", "Email column in file2.csv was not correctly redacted."
        assert "CONFIDENTIAL" in "".join(rows[0]), "Original CONFIDENTIAL data was lost in file2.csv."

    file3_path = os.path.join(archive_dir, "file3.json")
    assert not os.path.exists(file3_path), "file3.json should not have been archived."

def test_redis_manifest_contains_correct_checksums():
    # Calculate actual checksums of the archived files
    expected_hashes = {}
    for fname in ["file1.json", "file2.csv"]:
        filepath = f"/app/data/archive/{fname}"
        if os.path.isfile(filepath):
            expected_hashes[fname] = get_file_sha256(filepath)

    assert len(expected_hashes) == 2, "Expected 2 files to be archived for checksum verification."

    # Fetch hash from Redis using redis-cli
    try:
        output = subprocess.check_output(
            ["redis-cli", "HGETALL", "archive_manifest"], 
            text=True, 
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to query Redis: {e.output}"

    lines = [line.strip() for line in output.strip().split('\n') if line.strip()]
    redis_manifest = {}
    # redis-cli HGETALL returns key, value, key, value...
    for i in range(0, len(lines) - 1, 2):
        redis_manifest[lines[i]] = lines[i+1]

    for fname, expected_hash in expected_hashes.items():
        assert fname in redis_manifest, f"{fname} is missing from Redis archive_manifest."
        assert redis_manifest[fname] == expected_hash, f"Redis checksum for {fname} does not match the actual file's SHA-256."

def test_flask_api_manifest_endpoint():
    # Calculate actual checksums of the archived files
    expected_hashes = {}
    for fname in ["file1.json", "file2.csv"]:
        filepath = f"/app/data/archive/{fname}"
        if os.path.isfile(filepath):
            expected_hashes[fname] = get_file_sha256(filepath)

    assert len(expected_hashes) == 2, "Expected 2 files to be archived for API verification."

    try:
        response = requests.get("http://127.0.0.1:5000/manifest", timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to Flask API on port 5000: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 from /manifest, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type to be application/json"

    try:
        api_manifest = response.json()
    except ValueError:
        assert False, "Response from /manifest is not valid JSON."

    for fname, expected_hash in expected_hashes.items():
        assert fname in api_manifest, f"{fname} is missing from API /manifest response."
        assert api_manifest[fname] == expected_hash, f"API checksum for {fname} does not match the actual file's SHA-256."
# test_final_state.py

import os
import hashlib
import requests
import pytest
import time

def test_organized_data_files():
    # Verify the 50 files are organized correctly
    categories = ["syslogs", "metrics", "traces"]
    for i in range(1, 51):
        cat_idx = i % 3
        cat = categories[cat_idx]
        ts = 1680000000 + i
        file_path = f"/app/organized_data/{cat}/{ts}.log"
        assert os.path.isfile(file_path), f"Expected file {file_path} is missing."

        with open(file_path, 'r') as f:
            lines = f.readlines()
            assert lines[0].strip() == f"CATEGORY: {cat}"
            assert lines[1].strip() == f"TIMESTAMP: {ts}"

def test_processed_log():
    log_path = "/app/organized_data/processed.log"
    assert os.path.isfile(log_path), "processed.log is missing."

    with open(log_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 50, f"Expected 50 lines in processed.log, got {len(lines)}"

    # Check that all 50 expected lines are present (order may vary due to concurrency)
    categories = ["syslogs", "metrics", "traces"]
    expected_lines = set()
    for i in range(1, 51):
        cat_idx = i % 3
        cat = categories[cat_idx]
        ts = 1680000000 + i
        expected_lines.add(f"MOVED dump_{i}.dat TO {cat}/{ts}.log\n")

    actual_lines = set(lines)
    missing = expected_lines - actual_lines
    assert not missing, f"processed.log is missing expected entries: {missing}"

def test_manifest_file():
    manifest_path = "/app/organized_data/manifest.sha256"
    assert os.path.isfile(manifest_path), "manifest.sha256 is missing."

    with open(manifest_path, 'r') as f:
        manifest_lines = f.readlines()

    assert len(manifest_lines) == 50, f"Expected 50 entries in manifest.sha256, got {len(manifest_lines)}"

    # Recompute hashes
    categories = ["syslogs", "metrics", "traces"]
    expected_hashes = {}
    for i in range(1, 51):
        cat_idx = i % 3
        cat = categories[cat_idx]
        ts = 1680000000 + i
        rel_path = f"{cat}/{ts}.log"
        abs_path = f"/app/organized_data/{rel_path}"

        with open(abs_path, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
            expected_hashes[rel_path] = h

    parsed_manifest = {}
    for line in manifest_lines:
        parts = line.strip().split(maxsplit=1)
        assert len(parts) == 2, f"Invalid manifest line format: {line}"
        h, p = parts
        # Remove leading ./ if present
        if p.startswith("./"):
            p = p[2:]
        parsed_manifest[p] = h

    for p, h in expected_hashes.items():
        assert p in parsed_manifest, f"File {p} missing from manifest"
        assert parsed_manifest[p] == h, f"Hash mismatch for {p}: expected {h}, got {parsed_manifest[p]}"

def test_http_server_valid_token():
    url = "http://127.0.0.1:9090/manifest.sha256"
    headers = {"Authorization": "Bearer secret-token-88"}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code} with body: {resp.text}"
    assert "syslogs/1680000003.log" in resp.text, "Manifest content missing from response"

def test_http_server_invalid_token():
    url = "http://127.0.0.1:9090/manifest.sha256"
    # Provide a token that contains 'Bearer' but is not the exact token
    headers = {"Authorization": "Bearer fake-token"}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized for invalid token, got {resp.status_code}"

def test_http_server_missing_file():
    url = "http://127.0.0.1:9090/doesnotexist.log"
    headers = {"Authorization": "Bearer secret-token-88"}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    assert resp.status_code == 404, f"Expected 404 Not Found, got {resp.status_code}"
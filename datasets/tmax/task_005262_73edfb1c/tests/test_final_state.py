# test_final_state.py

import os
import requests
import pytest

def test_csv_conversion():
    legacy_path = "/app/artifact_manager/data/manifest.legacy"
    csv_path = "/app/artifact_manager/data/manifest.csv"

    assert os.path.exists(csv_path), f"{csv_path} does not exist. Did you create the CSV file?"

    # Read the legacy file to dynamically determine the expected output
    with open(legacy_path, "r", encoding="iso-8859-1") as f:
        legacy_lines = [line.strip() for line in f if line.strip()]

    expected_rows = ["File,Hash,Bytes"]
    for line in legacy_lines:
        expected_rows.append(line.replace("|", ","))

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            csv_lines = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        pytest.fail(f"{csv_path} is not valid UTF-8 encoded.")

    assert csv_lines == expected_rows, "CSV content does not match the expected transformation from the legacy file."

def test_http_artifact_download():
    binary_path = "/app/artifact_manager/data/binaries/test_artifact.bin"
    assert os.path.exists(binary_path), f"Truth binary {binary_path} is missing."

    with open(binary_path, "rb") as f:
        expected_content = f.read()

    url = "http://127.0.0.1:8000/api/artifact/test_artifact.bin"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}. Is Nginx running and configured correctly? Error: {e}")

    assert resp.status_code == 200, f"Expected HTTP status 200, got {resp.status_code}. Response: {resp.text[:100]}"

    content_type = resp.headers.get("Content-Type", "")
    assert "application/octet-stream" in content_type, f"Expected Content-Type to be application/octet-stream, got '{content_type}'"

    assert resp.content == expected_content, "The downloaded content does not match the local binary file."

def test_http_artifact_not_found():
    url = "http://127.0.0.1:8000/api/artifact/nonexistent_file_12345.bin"
    try:
        resp = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}. Error: {e}")

    assert resp.status_code == 404, f"Expected HTTP status 404 for a nonexistent file, got {resp.status_code}. Response: {resp.text[:100]}"
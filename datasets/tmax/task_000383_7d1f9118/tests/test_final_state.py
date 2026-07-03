# test_final_state.py

import os
import glob
import requests
import pytest

DOCS_DIR = "/home/user/extracted_docs"
PORT = 8080
TOKEN = "DocAuth992"
SIGN_OFF = "Drafted by TechWriter Pro"
BASE_URL = f"http://127.0.0.1:{PORT}"

def test_extracted_docs_directory_exists():
    assert os.path.isdir(DOCS_DIR), f"Directory {DOCS_DIR} does not exist. Did you extract the archives correctly?"

def test_txt_files_exist_and_processed():
    txt_files = glob.glob(os.path.join(DOCS_DIR, "*.txt"))
    assert len(txt_files) > 0, f"No .txt files found in {DOCS_DIR}."

    for file_path in txt_files:
        with open(file_path, "rb") as f:
            content_bytes = f.read()

        try:
            content_str = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail(f"File {file_path} is not valid UTF-8.")

        assert "[[TITLE:" not in content_str, f"Unreplaced [[TITLE:...]] macro found in {file_path}"
        assert "[[BOLD:" not in content_str, f"Unreplaced [[BOLD:...]] macro found in {file_path}"

        lines = content_str.strip().split("\n")
        assert lines[-1].strip() == SIGN_OFF, f"Sign-off phrase missing or incorrect at the end of {file_path}"

def test_server_unauthorized():
    # Test without auth header
    try:
        response = requests.get(f"{BASE_URL}/nonexistent.txt", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server on port {PORT}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth header, got {response.status_code}"

    # Test with invalid auth header
    headers = {"Authorization": "Bearer InvalidToken123"}
    response = requests.get(f"{BASE_URL}/nonexistent.txt", headers=headers, timeout=2)
    assert response.status_code == 401, f"Expected 401 Unauthorized for invalid auth header, got {response.status_code}"

def test_server_authorized_and_serves_files():
    txt_files = glob.glob(os.path.join(DOCS_DIR, "*.txt"))
    if not txt_files:
        pytest.skip("No .txt files to test server with.")

    headers = {"Authorization": f"Bearer {TOKEN}"}

    for file_path in txt_files:
        filename = os.path.basename(file_path)
        try:
            response = requests.get(f"{BASE_URL}/{filename}", headers=headers, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to server on port {PORT}: {e}")

        assert response.status_code == 200, f"Expected 200 OK for {filename}, got {response.status_code}"

        with open(file_path, "rb") as f:
            expected_content = f.read()

        assert response.content == expected_content, f"Served content for {filename} does not match the file on disk."
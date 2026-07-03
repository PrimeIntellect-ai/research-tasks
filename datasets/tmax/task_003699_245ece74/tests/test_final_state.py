# test_final_state.py

import os
import requests
import pytest

def test_quarantine():
    quarantine_file = "/home/user/quarantine/backup_2.tar"
    assert os.path.isfile(quarantine_file), f"Malicious archive was not moved to {quarantine_file}"

def test_renamed_html():
    old_html = "/home/user/extracted_docs/docs/old.html"
    assert os.path.isfile(old_html), f"File {old_html} is missing. It should have been renamed from .HTM"

def test_deleted_error_file():
    bad_doc = "/home/user/extracted_docs/docs/bad_doc.txt"
    assert not os.path.exists(bad_doc), f"File {bad_doc} should have been deleted based on the error log"

def test_api_index():
    url = "http://127.0.0.1:8080/api/index"
    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.text.startswith("MAGIC_INDEX_V1"), "Response does not start with MAGIC_INDEX_V1"

def test_api_docs():
    url = "http://127.0.0.1:8080/api/docs?file=old.html"
    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "<html>Old html</html>" in response.text, "Response does not contain the expected HTML content"
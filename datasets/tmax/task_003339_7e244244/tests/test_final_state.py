# test_final_state.py
import os
import tarfile
import tempfile
import requests
import pytest

def test_clean_logs_app1():
    path = "/home/user/clean_logs/2023-10-25/app1.log"
    assert os.path.isfile(path), f"File {path} not found. The log file was not correctly processed and moved."
    with open(path, "r") as f:
        content = f.read()
    assert "[2023-10-25 10:15:30]" in content, "Timestamps in app1.log were not correctly standardized to YYYY-MM-DD."
    assert "END_OF_TRANSACTION" in content, "END_OF_TRANSACTION missing from app1.log."

def test_clean_logs_app2():
    path = "/home/user/clean_logs/2023-10-26/app2.log"
    assert os.path.isfile(path), f"File {path} not found. The compliant log file was not correctly moved."
    with open(path, "r") as f:
        content = f.read()
    assert "[2023-10-26 11:00:00]" in content, "Timestamps in app2.log were altered incorrectly."

def test_clean_logs_app3():
    path = "/home/user/clean_logs/2023-10-27/app3.log"
    assert not os.path.isfile(path), f"File {path} should have been discarded because it was not compliant."

def test_api_unauthorized():
    try:
        resp = requests.get("http://127.0.0.1:8080/download?date=2023-10-25")
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the Rust API at 127.0.0.1:8080")

    assert resp.status_code == 401, f"Expected 401 Unauthorized without Auth header, got {resp.status_code}"

def test_api_download_authorized():
    headers = {"Authorization": "Bearer project-alpha-99"}
    try:
        resp = requests.get("http://127.0.0.1:8080/download?date=2023-10-25", headers=headers)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the Rust API at 127.0.0.1:8080")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    assert "gzip" in resp.headers.get("Content-Type", ""), f"Expected application/gzip content type, got {resp.headers.get('Content-Type')}"

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(resp.content)
        tmp_path = tmp.name

    try:
        with tarfile.open(tmp_path, "r:gz") as tar:
            names = tar.getnames()
            assert any("app1.log" in name for name in names), f"app1.log not found in the downloaded archive. Found: {names}"
    except tarfile.ReadError:
        pytest.fail("The downloaded file is not a valid gzip tar archive.")
    finally:
        os.remove(tmp_path)

def test_api_verify():
    headers = {"Authorization": "Bearer project-alpha-99"}
    payload = {"path": "/home/user/clean_logs/2023-10-26/app2.log"}
    try:
        resp = requests.post("http://127.0.0.1:8080/verify", headers=headers, json=payload)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the Rust API at 127.0.0.1:8080")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Expected JSON response from /verify endpoint.")

    assert data.get("status") == "compliant", f"Expected status 'compliant', got {data.get('status')}"
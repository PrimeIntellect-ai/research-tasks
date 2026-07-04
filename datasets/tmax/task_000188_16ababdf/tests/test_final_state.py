# test_final_state.py
import os
import requests
import pytest

REPO_DIR = "/home/user/repo"
SERVER_URL = "http://127.0.0.1:8000"

def test_repo_directory_contents():
    assert os.path.isdir(REPO_DIR), f"Directory {REPO_DIR} does not exist."
    files = sorted(os.listdir(REPO_DIR))
    expected_files = ["approved_1.elf.pkg", "approved_2.gcode.pkg"]
    assert files == expected_files, f"Expected files {expected_files} in {REPO_DIR}, but found {files}."

def test_server_manifest():
    url = f"{SERVER_URL}/manifest"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 for /manifest, got {response.status_code}."
    try:
        manifest = response.json()
    except ValueError:
        pytest.fail("Response from /manifest is not valid JSON.")

    expected_manifest = ["approved_1.elf.pkg", "approved_2.gcode.pkg"]
    assert manifest == expected_manifest, f"Expected manifest {expected_manifest}, got {manifest}."

def test_server_artifact_elf():
    filename = "approved_1.elf.pkg"
    url = f"{SERVER_URL}/artifact/{filename}"
    filepath = os.path.join(REPO_DIR, filename)

    assert os.path.isfile(filepath), f"Expected packed file {filepath} does not exist."
    with open(filepath, "rb") as f:
        expected_content = f.read()

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 for {url}, got {response.status_code}."
    assert response.content == expected_content, f"Content from {url} does not match the file on disk."

def test_server_artifact_gcode():
    filename = "approved_2.gcode.pkg"
    url = f"{SERVER_URL}/artifact/{filename}"
    filepath = os.path.join(REPO_DIR, filename)

    assert os.path.isfile(filepath), f"Expected packed file {filepath} does not exist."
    with open(filepath, "rb") as f:
        expected_content = f.read()

    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 for {url}, got {response.status_code}."
    assert response.content == expected_content, f"Content from {url} does not match the file on disk."

def test_server_artifact_not_found():
    url = f"{SERVER_URL}/artifact/nonexistent_file.pkg"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 404, f"Expected status 404 for missing file, got {response.status_code}."
# test_final_state.py

import os
import tarfile
import requests
import pytest
import time

def test_backup_tarball_exists_and_valid():
    """Check that the backup tarball was created and is a valid tar.gz file."""
    tarball_path = "/home/user/nginx_backup.tar.gz"
    assert os.path.isfile(tarball_path), f"Backup tarball not found at {tarball_path}."

    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            members = tar.getnames()
            assert len(members) > 0, "The backup tarball is empty."
    except tarfile.ReadError:
        pytest.fail(f"The file at {tarball_path} is not a valid gzip-compressed tarball.")

def test_nginx_authorized_request():
    """Check that NGINX returns 200 OK when the correct Authorization header is provided."""
    url = "http://127.0.0.1:8080/"
    headers = {"Authorization": "Bearer alpha-tango-niner"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to NGINX at {url}. Is NGINX running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK with correct token, but got {response.status_code}."

def test_nginx_unauthorized_request_missing_header():
    """Check that NGINX returns 401 Unauthorized when the Authorization header is missing."""
    url = "http://127.0.0.1:8080/"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to NGINX at {url}. Is NGINX running? Error: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized with missing token, but got {response.status_code}."

def test_nginx_unauthorized_request_invalid_token():
    """Check that NGINX returns 401 Unauthorized when an incorrect Authorization header is provided."""
    url = "http://127.0.0.1:8080/"
    headers = {"Authorization": "Bearer wrong-token"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to NGINX at {url}. Is NGINX running? Error: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized with incorrect token, but got {response.status_code}."
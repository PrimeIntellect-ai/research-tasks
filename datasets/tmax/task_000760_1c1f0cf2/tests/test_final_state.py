# test_final_state.py

import os
import requests
import pytest

def test_organized_directory_structure():
    """Verify that the organized directory structure exists and contains the expected files."""
    organized_dir = "/home/user/organized_project"

    assert os.path.isdir(organized_dir), f"Organized directory not found at {organized_dir}"

    expected_files = [
        "logs/app.log",
        "src/main.py",
        "README.md"
    ]

    for rel_path in expected_files:
        full_path = os.path.join(organized_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected file not found at {full_path}"

def test_http_server_serving_files():
    """Verify that the HTTP server is running and serving the expected files."""
    base_url = "http://127.0.0.1:8080"

    endpoints = [
        "/logs/app.log",
        "/src/main.py",
        "/README.md"
    ]

    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to HTTP server at {url}. Error: {e}")

        assert response.status_code == 200, f"Expected 200 OK for {url}, got {response.status_code}"
        assert len(response.content) > 0, f"Response content for {url} is empty"
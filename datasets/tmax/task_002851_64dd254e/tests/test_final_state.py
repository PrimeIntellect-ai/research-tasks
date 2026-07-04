# test_final_state.py

import os
import subprocess
import requests
import pytest
import time

def test_directory_structure_and_config():
    """Verify the directory structure and configuration file exist."""
    releases_dir = "/home/user/app/releases/v2"
    current_link = "/home/user/app/current"
    config_file = "/home/user/app/current/config.txt"

    assert os.path.isdir(releases_dir), f"Directory {releases_dir} does not exist."
    assert os.path.islink(current_link), f"{current_link} is not a symlink."
    assert os.readlink(current_link) == releases_dir, f"{current_link} does not point to {releases_dir}."

    assert os.path.isfile(config_file), f"Config file {config_file} does not exist."
    with open(config_file, "r") as f:
        content = f.read().strip()
    assert content == "IMAGE=/app/target_image.png", f"Config file content is incorrect: {content}"

def test_c_server_binary_exists():
    """Verify the C server was compiled."""
    binary_path = "/home/user/app/current/server"
    assert os.path.isfile(binary_path), f"C server binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"C server binary {binary_path} is not executable."

def test_http_service_and_tunnel():
    """Verify the HTTP service is accessible via the SSH tunnel and returns correct OCR data."""
    # Run tesseract directly to get the expected output
    image_path = "/app/target_image.png"
    assert os.path.isfile(image_path), f"Target image {image_path} is missing."

    result = subprocess.run(["tesseract", image_path, "stdout"], capture_output=True, text=True)
    expected_text = result.stdout.strip()

    # Give the service a moment to be ready if needed, though it should already be running
    url = "http://127.0.0.1:9090/extract"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    actual_text = response.text.strip()
    assert expected_text in actual_text or "CONFIDENTIAL-KEY-8842-OMEGA" in actual_text, \
        f"Expected OCR text not found in response. Got: {actual_text}"

def test_http_service_404():
    """Verify the HTTP service returns 404 for unknown endpoints."""
    url = "http://127.0.0.1:9090/unknown_endpoint"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 404, f"Expected status code 404 for unknown endpoint, got {response.status_code}"
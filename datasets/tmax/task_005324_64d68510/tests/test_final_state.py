# test_final_state.py

import os
import hashlib
import requests
import pytest

def get_md5(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def test_output_files_exist_and_correct():
    """Test that the generated output files exist and have correct content."""
    expected_files = [
        "/app/output/en/WELCOME_MSG.txt",
        "/app/output/es/WELCOME_MSG.txt",
        "/app/output/es/ERR_01.txt"
    ]

    for path in expected_files:
        assert os.path.exists(path), f"Expected output file missing: {path}"
        assert os.path.isfile(path), f"Expected output path is not a file: {path}"

    unexpected_file = "/app/output/es/WELCOME_ALT.txt"
    assert not os.path.exists(unexpected_file), f"Unexpected file exists (should have been deduplicated): {unexpected_file}"

def test_output_file_content():
    """Test the exact content of an output file."""
    path = "/app/output/es/ERR_01.txt"
    assert os.path.exists(path), f"Missing file: {path}"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_content = (
        "Release: v7.4.2-RCO\n"
        "Locale: es\n"
        "String ID: ERR_01\n"
        "\n"
        "Archivo\n"
        "no encontrado"
    )

    assert content.strip() == expected_content.strip(), f"Content of {path} does not match expected templated output."

def test_pipeline_log():
    """Test that the pipeline log exists and contains the correct entries."""
    path = "/app/pipeline.log"
    assert os.path.exists(path), f"Missing log file: {path}"

    with open(path, "r", encoding="utf-8") as f:
        log_content = f.read()

    hash_welcome = get_md5("Welcome to the app!")
    hash_err = get_md5("File not found")

    expected_logs = [
        f"[PROCESS] Created template for en - WELCOME_MSG (Hash: {hash_welcome})",
        f"[PROCESS] Created template for es - WELCOME_MSG (Hash: {hash_welcome})",
        f"[PROCESS] Created template for es - ERR_01 (Hash: {hash_err})"
    ]

    for expected in expected_logs:
        assert expected in log_content, f"Expected log entry not found: {expected}"

def test_http_server_serving_files():
    """Test that the HTTP server is running and serving the generated files."""
    url = "http://127.0.0.1:9090/es/ERR_01.txt"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    expected_content = (
        "Release: v7.4.2-RCO\n"
        "Locale: es\n"
        "String ID: ERR_01\n"
        "\n"
        "Archivo\n"
        "no encontrado"
    )

    assert response.text.strip() == expected_content.strip(), "HTTP response content does not match expected output file content."
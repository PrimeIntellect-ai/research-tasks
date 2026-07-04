# test_final_state.py

import os
import socket
import requests
import pytest

def test_http_endpoint_unauthorized():
    """Test that the HTTP endpoint rejects requests without the proper token."""
    url = "http://127.0.0.1:8080/api/v1/docs/syslog_extract.md"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on port 8080: {e}")

    assert response.status_code in (401, 403), f"Expected 401 or 403 for unauthorized request, got {response.status_code}"

def test_http_endpoint_authorized():
    """Test that the HTTP endpoint serves the document with the proper token."""
    url = "http://127.0.0.1:8080/api/v1/docs/syslog_extract.md"
    headers = {"Authorization": "Bearer TECH-WRITE-2024"}
    try:
        response = requests.get(url, headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to HTTP server on port 8080: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    assert len(response.text) > 0, "Expected non-empty response body"

def test_grpc_port_listening():
    """Test that the gRPC server is listening on port 9090."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', 9090))
        assert result == 0, "gRPC server is not listening on port 9090"

def test_decoder_script_exists():
    """Test that the Go decoder script was created."""
    decoder_path = "/home/user/decoder.go"
    assert os.path.exists(decoder_path), f"Decoder script not found at {decoder_path}"

def test_processed_docs_directory():
    """Test that the processed_docs directory exists and contains files."""
    docs_dir = "/home/user/processed_docs"
    assert os.path.exists(docs_dir), f"Processed docs directory not found at {docs_dir}"
    assert os.path.isdir(docs_dir), f"{docs_dir} is not a directory"

    # Check if there's at least one markdown file
    md_files = [f for f in os.listdir(docs_dir) if f.endswith('.md')]
    assert len(md_files) > 0, "No markdown files found in processed_docs directory"
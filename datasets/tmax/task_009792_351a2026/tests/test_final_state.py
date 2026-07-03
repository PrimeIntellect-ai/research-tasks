# test_final_state.py

import os
import sys
import urllib.request
import urllib.error
import subprocess
import pytest

def test_fast_hash_installed_and_working():
    # Attempt to import the installed fast_hash module
    try:
        import fast_hash
    except ImportError:
        pytest.fail("The 'fast_hash' module could not be imported. Did you install the package?")

    # Test the logic
    assert hasattr(fast_hash, 'fast_hash'), "Module 'fast_hash' does not have function 'fast_hash'"
    test_str = "2023-10-01T10:00:05 WARN High memory"
    expected_hash = sum(ord(c) for c in test_str) % 256

    try:
        actual_hash = fast_hash.fast_hash(test_str)
    except Exception as e:
        pytest.fail(f"Calling fast_hash failed: {e}")

    assert actual_hash == expected_hash, f"fast_hash returned {actual_hash}, expected {expected_hash}. C extension logic is incorrect."

def test_merged_log_content():
    merged_path = "/home/user/workspace/output/merged.log"
    assert os.path.isfile(merged_path), f"Merged log file not found at {merged_path}"

    with open(merged_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[105] 2023-10-01T10:00:01 INFO DB connected",
        "[114] 2023-10-01T10:00:02 INFO App started",
        "[152] 2023-10-01T10:00:04 ERROR Connection lost",
        "[242] 2023-10-01T10:00:05 WARN High memory"
    ]

    assert lines == expected_lines, "The content of merged.log does not match the expected sorted and hashed output."

def test_diff_txt_content():
    diff_path = "/home/user/workspace/output/diff.txt"
    assert os.path.isfile(diff_path), f"Diff file not found at {diff_path}"

    with open(diff_path, "r") as f:
        content = f.read()

    # Check that diff contains the differences between baseline and merged
    assert "065" in content and "Normal memory" in content, "diff.txt does not contain the removed baseline line."
    assert "242" in content and "WARN High memory" in content, "diff.txt does not contain the added merged line."

def test_python_http_server_port_9000():
    try:
        response = urllib.request.urlopen("http://127.0.0.1:9000/diff.txt", timeout=2)
        assert response.status == 200, "Python HTTP server did not return 200 OK for diff.txt"
        content = response.read().decode('utf-8')
        assert "Normal memory" in content and "WARN High memory" in content, "Python HTTP server did not serve the correct diff.txt content."
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Python HTTP server on port 9000: {e}")

def test_nginx_reverse_proxy_port_8080():
    try:
        response = urllib.request.urlopen("http://127.0.0.1:8080/diff.txt", timeout=2)
        assert response.status == 200, "Nginx reverse proxy did not return 200 OK for diff.txt"
        content = response.read().decode('utf-8')
        assert "Normal memory" in content and "WARN High memory" in content, "Nginx reverse proxy did not serve the correct diff.txt content."

        # Verify it's Nginx serving
        server_header = response.getheader('Server')
        if server_header:
            assert 'nginx' in server_header.lower(), f"Expected Nginx server header, got {server_header}"
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Nginx reverse proxy on port 8080: {e}")

def test_nginx_conf_exists():
    conf_path = "/home/user/workspace/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx configuration file not found at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "8080" in content, "Nginx config does not contain port 8080."
    assert "9000" in content, "Nginx config does not contain proxy pass to port 9000."
    assert "nginx_temp" in content, "Nginx config does not use nginx_temp directory for temp files."
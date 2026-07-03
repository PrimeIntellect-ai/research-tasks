# test_final_state.py
import os
import tarfile
import gzip
import io
import requests
import pytest

API_URL = "http://127.0.0.1:8134"
AUTH_TOKEN = "sec_bkup_992a1"
HEADERS_VALID = {"Authorization": f"Bearer {AUTH_TOKEN}"}
HEADERS_INVALID = {"Authorization": "Bearer invalid"}

def test_api_config_txt():
    """Test that config.txt is correctly served via the API."""
    url = f"{API_URL}/download/config.txt"
    try:
        response = requests.get(url, headers=HEADERS_VALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert response.text.strip() == "system=ready", f"Unexpected content for config.txt: {response.text}"

def test_api_unauthorized():
    """Test that the API rejects unauthorized requests."""
    url = f"{API_URL}/download/config.txt"
    try:
        response = requests.get(url, headers=HEADERS_INVALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid token, got {response.status_code}"

def test_api_merged_log():
    """Test that the merged log is correctly served via the API."""
    url = f"{API_URL}/download/logs/server_complete.log"
    try:
        response = requests.get(url, headers=HEADERS_VALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    expected_content = "Line 1\nLine 2\nLine 3\nLine 4\n"
    assert response.text.replace("\r\n", "\n") == expected_content, f"Unexpected content for merged log: {response.text}"

def test_api_path_traversal():
    """Test that the API rejects path traversal attempts or correctly returns 404/403."""
    url = f"{API_URL}/download/../../../etc/shadow"
    try:
        response = requests.get(url, headers=HEADERS_VALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code in (404, 403), f"Expected HTTP 404 or 403 for path traversal, got {response.status_code}"

def test_api_logs_archive():
    """Test that the logs archive is correctly served and is a valid tar.gz."""
    url = f"{API_URL}/download/logs_archive.tar.gz"
    try:
        response = requests.get(url, headers=HEADERS_VALID, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    # Check if it's a valid gzip and tar
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as gz:
            with tarfile.open(fileobj=gz, mode="r") as tar:
                names = tar.getnames()
                # Ensure some log files are present in the tar
                assert any("server.log.part1" in name for name in names), "server.log.part1 missing in archive"
                assert any("server.log.part2" in name for name in names), "server.log.part2 missing in archive"
    except Exception as e:
        pytest.fail(f"Failed to parse logs_archive.tar.gz: {e}")

def test_local_filesystem_safe_extraction():
    """Test that malicious files were not extracted to the local filesystem."""
    extracted_safe_dir = "/home/user/extracted_safe"
    assert os.path.isdir(extracted_safe_dir), f"Directory {extracted_safe_dir} does not exist"

    # Check that config.txt exists
    assert os.path.isfile(os.path.join(extracted_safe_dir, "config.txt")), "config.txt not found in extracted_safe"

    # Check that malicious files were NOT extracted
    malicious_path_1 = "/home/user/extracted_safe/../../../etc/shadow"
    malicious_path_2 = "/home/user/extracted_safe/var/log/syslog"
    assert not os.path.exists(os.path.abspath(malicious_path_1)), "Malicious file extracted via path traversal!"
    assert not os.path.exists(malicious_path_2), "Malicious absolute path file extracted!"
# test_final_state.py

import os
import json
import tarfile
import urllib.request
import urllib.error
import time
import pytest

REPORT_PATH = "/home/user/update_report.json"
UPDATED_ARCHIVE_PATH = "/home/user/updated_docs.tar.gz"
SERVER_URL = "http://localhost:8080/update_report.json"

def test_report_exists_and_correct():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    with open(REPORT_PATH, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {REPORT_PATH} is not valid JSON.")

    expected_data = {
        "docs/api/endpoints.md": 2,
        "docs/guides/setup.md": 1
    }

    assert report_data == expected_data, f"Report data {report_data} does not match expected {expected_data}."

def test_updated_archive_exists_and_correct():
    assert os.path.exists(UPDATED_ARCHIVE_PATH), f"Updated archive {UPDATED_ARCHIVE_PATH} does not exist."
    assert tarfile.is_tarfile(UPDATED_ARCHIVE_PATH), f"{UPDATED_ARCHIVE_PATH} is not a valid tar file."

    with tarfile.open(UPDATED_ARCHIVE_PATH, "r:gz") as tar:
        names = tar.getnames()

        # Check files that should be included
        assert "docs/api/endpoints.md" in names, "docs/api/endpoints.md is missing from the updated archive."
        assert "docs/guides/setup.md" in names, "docs/guides/setup.md is missing from the updated archive."

        # Check files that should NOT be included
        assert "docs/api/new_endpoints.md" not in names, "docs/api/new_endpoints.md should not be in the updated archive."
        assert "docs/readme.md" not in names, "docs/readme.md should not be in the updated archive."

        # Check contents of docs/api/endpoints.md
        f = tar.extractfile("docs/api/endpoints.md")
        assert f is not None, "Could not extract docs/api/endpoints.md"
        content = f.read().decode("utf-8")

        assert "Status: Deprecated" in content, "Status was not changed to Deprecated in docs/api/endpoints.md."
        assert "Status: Active" not in content, "Status: Active is still present in docs/api/endpoints.md."
        assert "https://api.new.local/v2/users" in content, "API URL was not updated correctly in docs/api/endpoints.md."
        assert "http://api.old.local/v1/" not in content, "Legacy API URL is still present in docs/api/endpoints.md."

        # Check contents of docs/guides/setup.md
        f2 = tar.extractfile("docs/guides/setup.md")
        assert f2 is not None, "Could not extract docs/guides/setup.md"
        content2 = f2.read().decode("utf-8")

        assert "Status: Deprecated" in content2, "Status was not changed to Deprecated in docs/guides/setup.md."
        assert "https://api.new.local/v2/downloads" in content2, "API URL was not updated correctly in docs/guides/setup.md."

def test_http_server_running():
    max_retries = 3
    for i in range(max_retries):
        try:
            req = urllib.request.Request(SERVER_URL)
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status == 200, f"Server returned status {response.status}"
                data = response.read().decode("utf-8")
                report_data = json.loads(data)
                expected_data = {
                    "docs/api/endpoints.md": 2,
                    "docs/guides/setup.md": 1
                }
                assert report_data == expected_data, "Server did not serve the correct update_report.json content."
            return
        except (urllib.error.URLError, ConnectionResetError, json.JSONDecodeError) as e:
            if i == max_retries - 1:
                pytest.fail(f"Failed to connect to server at {SERVER_URL} or invalid response: {e}")
            time.sleep(1)
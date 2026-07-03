# test_final_state.py

import os
import io
import tarfile
import requests
import pytest

def test_pylogarchiver_bug_fixed():
    locker_file = "/app/pylogarchiver-1.0.0/pylogarchiver/locker.py"
    assert os.path.isfile(locker_file), f"File {locker_file} is missing."

    with open(locker_file, "r") as f:
        content = f.read()

    # Check if the bug is fixed (bitwise OR instead of AND)
    assert "fcntl.LOCK_EX | fcntl.LOCK_NB" in content, "The bug in locker.py was not fixed. Expected 'fcntl.LOCK_EX | fcntl.LOCK_NB'."
    assert "fcntl.LOCK_EX & fcntl.LOCK_NB" not in content, "The bug in locker.py is still present."

def test_service_download_endpoint():
    url = "http://127.0.0.1:8080/download"
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text[:200]}"

    # Verify the response is a valid tar.gz
    try:
        tar_stream = io.BytesIO(response.content)
        with tarfile.open(fileobj=tar_stream, mode="r:gz") as tar:
            members = tar.getmembers()
            assert len(members) > 0, "The returned tar.gz archive is empty."

            # Check for files
            files = [m for m in members if m.isfile()]
            assert len(files) > 0, "No files found in the tar.gz archive."

            for file_member in files:
                f = tar.extractfile(file_member)
                assert f is not None, f"Failed to extract {file_member.name} from archive."
                content = f.read()
                # If there is content, ensure it doesn't have torn lines (assuming lines end with \n)
                if len(content) > 0:
                    assert content.endswith(b"\n"), f"File {file_member.name} contains a torn line at the end."

    except tarfile.TarError as e:
        pytest.fail(f"The response body is not a valid tar.gz archive: {e}")
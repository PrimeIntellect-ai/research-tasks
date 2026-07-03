# test_final_state.py

import os
import io
import tarfile
import hashlib
import requests
import pytest

DATASET_DIR = "/home/user/dataset_active"
SERVER_URL = "http://127.0.0.1:8080/archive"
TOKEN = "ds-secret-token"

def get_file_checksum(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def test_server_running_and_returns_tar():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(SERVER_URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {SERVER_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text[:100]}"

    try:
        tar_stream = io.BytesIO(response.content)
        with tarfile.open(fileobj=tar_stream, mode="r") as tar:
            tar_members = tar.getmembers()
            assert len(tar_members) > 0, "Tar archive is empty."

            # Extract to a dict for easy lookup
            tar_files = {}
            for member in tar_members:
                # Strip leading slash or dot slash if present, to match relative paths
                name = member.name.lstrip("./")
                tar_files[name] = member

            # Walk the dataset dir and verify each file/symlink is in the tar
            for root, dirs, files in os.walk(DATASET_DIR):
                for name in files + dirs:
                    abs_path = os.path.join(root, name)
                    rel_path = os.path.relpath(abs_path, DATASET_DIR)

                    if rel_path == ".":
                        continue

                    assert rel_path in tar_files, f"Expected path '{rel_path}' not found in the tar archive."

                    member = tar_files[rel_path]

                    if os.path.islink(abs_path):
                        target = os.readlink(abs_path)
                        assert member.issym(), f"Expected '{rel_path}' to be a symlink in the tar archive."
                        assert member.linkname == target, f"Symlink '{rel_path}' target mismatch. Expected '{target}', got '{member.linkname}'."
                    elif os.path.isfile(abs_path):
                        assert member.isfile(), f"Expected '{rel_path}' to be a regular file in the tar archive."
                        assert member.size == os.path.getsize(abs_path), f"File size mismatch for '{rel_path}'."

                        # Verify checksum
                        f_tar = tar.extractfile(member)
                        assert f_tar is not None, f"Could not extract file '{rel_path}' from tar archive."
                        tar_content = f_tar.read()

                        tar_hasher = hashlib.sha256(tar_content)
                        expected_checksum = get_file_checksum(abs_path)
                        assert tar_hasher.hexdigest() == expected_checksum, f"Checksum mismatch for '{rel_path}'."

    except tarfile.ReadError:
        pytest.fail("The response could not be parsed as a valid tar archive.")
# test_final_state.py

import os
import socket
import tarfile
import pytest

def test_no_path_traversal():
    """Ensure the malicious file was not extracted outside the target directory."""
    path = "/home/user/hacked.txt"
    assert not os.path.exists(path), f"Path traversal vulnerability triggered: {path} exists."

def test_docs_clean_files_and_content():
    """Verify files were extracted and modified correctly."""
    docs_dir = "/home/user/docs_clean"
    expected_files = ["index.md", "api.md", "new_feature.md"]

    for f in expected_files:
        filepath = os.path.join(docs_dir, f)
        assert os.path.isfile(filepath), f"Expected file {filepath} is missing."

        with open(filepath, "r") as file:
            content = file.read()

        assert "DRAFT_STATUS: FINAL" in content, f"File {filepath} does not contain 'DRAFT_STATUS: FINAL'."
        assert "DRAFT_STATUS: INCOMPLETE" not in content, f"File {filepath} still contains 'DRAFT_STATUS: INCOMPLETE'."

        if f == "index.md":
            assert "Welcome to the project v2." in content, f"File {filepath} does not contain expected updated content."

def test_patch_tar_gz_exists_and_contents():
    """Verify the incremental backup archive exists and contains the differing files."""
    archive_path = "/home/user/patch.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} is missing."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()

    # Since all files in docs_clean were modified (DRAFT_STATUS changed) or are new,
    # they all differ from docs_original.
    expected_basenames = {"index.md", "api.md", "new_feature.md"}
    found_basenames = {os.path.basename(name) for name in names if name.endswith(".md")}

    missing = expected_basenames - found_basenames
    assert not missing, f"Archive {archive_path} is missing expected files: {missing}"

def test_tcp_server_correct_code():
    """Verify the TCP server grants access with the correct secret code."""
    index_path = "/home/user/docs_clean/index.md"
    assert os.path.isfile(index_path), f"Cannot test server: {index_path} missing."

    with open(index_path, "r") as f:
        expected_doc_content = f.read()

    try:
        with socket.create_connection(("127.0.0.1", 8000), timeout=3) as s:
            s.sendall(b"PROJECT_CODE: blue flying eagle\n")
            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
    except ConnectionRefusedError:
        pytest.fail("TCP server is not listening on port 8000.")
    except socket.timeout:
        pytest.fail("TCP server timed out while waiting for a response.")

    response_str = response.decode("utf-8", errors="replace")
    assert response_str.startswith("ACCESS_GRANTED\n"), f"Expected ACCESS_GRANTED response, got: {response_str[:50]}"
    assert expected_doc_content in response_str, "Server response did not contain the content of index.md."

def test_tcp_server_incorrect_code():
    """Verify the TCP server denies access with an incorrect secret code."""
    try:
        with socket.create_connection(("127.0.0.1", 8000), timeout=3) as s:
            s.sendall(b"PROJECT_CODE: wrong code\n")
            response = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
    except ConnectionRefusedError:
        pytest.fail("TCP server is not listening on port 8000.")
    except socket.timeout:
        pytest.fail("TCP server timed out while waiting for a response.")

    response_str = response.decode("utf-8", errors="replace").strip()
    assert response_str == "ACCESS_DENIED", f"Expected ACCESS_DENIED, got: {response_str}"
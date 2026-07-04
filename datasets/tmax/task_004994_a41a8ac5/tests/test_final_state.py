# test_final_state.py

import os
import gzip
import pytest

def test_merged_archive_exists_and_valid():
    merged_path = "/home/user/workspace/merged.tar.gz"
    assert os.path.exists(merged_path), f"Merged archive {merged_path} does not exist."
    assert os.path.isfile(merged_path), f"Path {merged_path} is not a file."

    # Check if it's a valid gzip file
    try:
        with gzip.open(merged_path, 'rb') as f:
            f.read(1)
    except Exception as e:
        pytest.fail(f"Merged archive is not a valid gzip file: {e}")

def test_valid_file_extracted():
    yaml_path = "/home/user/workspace/safe_configs/config/server.yaml"
    assert os.path.exists(yaml_path), f"Valid file {yaml_path} was not extracted."
    assert os.path.isfile(yaml_path), f"Path {yaml_path} is not a regular file."

    with open(yaml_path, 'r') as f:
        content = f.read()

    assert "host: localhost" in content, "The extracted server.yaml does not contain the expected content."
    assert "port: 8080" in content, "The extracted server.yaml does not contain the expected content."

def test_valid_symlink_extracted():
    symlink_path = "/home/user/workspace/safe_configs/config/link_to_server"
    # os.path.lexists checks if the symlink exists, even if broken
    assert os.path.lexists(symlink_path), f"Symlink {symlink_path} was not extracted."
    assert os.path.islink(symlink_path), f"Path {symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    assert target == "server.yaml", f"Symlink target is {target}, expected 'server.yaml'."

def test_extraction_log_contains_skipped_entries():
    log_path = "/home/user/workspace/extraction.log"
    assert os.path.exists(log_path), f"Extraction log {log_path} does not exist."
    assert os.path.isfile(log_path), f"Path {log_path} is not a file."

    with open(log_path, 'r') as f:
        log_content = f.read().splitlines()

    expected_skipped = [
        "SKIPPED: ../escaped_secret.txt",
        "SKIPPED: /etc/fake_passwd",
        "SKIPPED: config/link_to_root"
    ]

    for expected in expected_skipped:
        assert expected in log_content, f"Expected log entry '{expected}' not found in {log_path}."

def test_malicious_files_not_extracted():
    # Check that the path traversal file was not extracted to the workspace root
    escaped_secret_path = "/home/user/workspace/escaped_secret.txt"
    assert not os.path.exists(escaped_secret_path), "Path traversal vulnerability: escaped_secret.txt was extracted outside the safe_configs directory."

    # Check that the absolute path file was not extracted to /etc
    fake_passwd_path = "/etc/fake_passwd"
    assert not os.path.exists(fake_passwd_path), "Absolute path vulnerability: fake_passwd was extracted to /etc."

    # Check that the malicious symlink pointing to /etc was not extracted as a directory or file that allows traversal
    # The symlink itself might be extracted if the extractor failed to check it, but we already verify it's in the SKIPPED log.
    # We can also verify it doesn't exist in the safe_configs dir.
    malicious_symlink_path = "/home/user/workspace/safe_configs/config/link_to_root"
    assert not os.path.lexists(malicious_symlink_path), "Malicious symlink was extracted despite pointing outside the destination directory."
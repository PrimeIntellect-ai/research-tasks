# test_final_state.py
import os
import gzip
import base64
import pytest

def test_malicious_path_txt():
    path = "/home/user/malicious_path.txt"
    assert os.path.exists(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "../../../../home/user/evil.sh", f"Incorrect malicious path found: {content}"

def test_changelog_extracted():
    path = "/home/user/changelog.log"
    assert os.path.exists(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "Updated security protocols" in content, "changelog.log does not contain expected content."

def test_target_record_txt():
    path = "/home/user/target_record.txt"
    assert os.path.exists(path), f"File missing: {path}"
    with open(path, "r") as f:
        content = f.read().strip()

    assert "Updated security protocols" in content, "target_record.txt missing expected phrase."
    assert "---" not in content, "target_record.txt should not contain the '---' separators."
    assert "Commit: 124" in content, "target_record.txt missing 'Commit: 124'."
    assert "Commit: 123" not in content, "target_record.txt contains other records."
    assert "Commit: 125" not in content, "target_record.txt contains other records."

def test_record_custom_gz():
    record_path = "/home/user/target_record.txt"
    gz_path = "/home/user/record_custom.gz"

    assert os.path.exists(gz_path), f"File missing: {gz_path}"

    with open(record_path, "rb") as f:
        expected_raw = f.read()

    try:
        with gzip.open(gz_path, "rb") as f:
            decompressed_content = f.read()
    except Exception as e:
        pytest.fail(f"Failed to decompress {gz_path}: {e}")

    try:
        decoded_content = base64.b64decode(decompressed_content)
    except Exception as e:
        pytest.fail(f"Failed to base64 decode the decompressed content: {e}")

    assert decoded_content == expected_raw, "The decoded content of the gzipped base64 does not match target_record.txt"
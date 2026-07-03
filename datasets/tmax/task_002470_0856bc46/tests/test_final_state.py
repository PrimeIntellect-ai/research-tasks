# test_final_state.py

import os
import hashlib
import tarfile
import pytest

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_archiver_c_exists_and_uses_rename():
    c_file = "/home/user/archiver.c"
    assert os.path.isfile(c_file), f"{c_file} is missing."
    with open(c_file, "r") as f:
        content = f.read()
    assert "rename(" in content, "The C program must use the rename() function for atomic writes."

def test_manifest_content():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"{manifest_path} is missing."

    expected_files = ["network.conf", "cache.conf"]
    expected_lines = set()
    for filename in expected_files:
        filepath = os.path.join("/home/user/configs", filename)
        assert os.path.isfile(filepath), f"Expected config file {filepath} is missing."
        file_hash = get_sha256(filepath)
        # sha256sum outputs two spaces between hash and filename
        expected_lines.add(f"{file_hash}  {filename}")

    with open(manifest_path, "r") as f:
        manifest_lines = set(line.strip() for line in f if line.strip())

    # Some implementations might use a single space or asterisk, but the prompt says:
    # "The format must be exactly what sha256sum outputs: <hash>  <filename>"

    assert manifest_lines == expected_lines, (
        f"Manifest contents do not match expected.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {manifest_lines}"
    )

def test_tarball_content():
    tarball_path = "/home/user/incremental.tar.gz"
    assert os.path.isfile(tarball_path), f"{tarball_path} is missing."

    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            members = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"{tarball_path} is not a valid gzip-compressed tarball.")

    expected_members = {"network.conf", "cache.conf"}
    actual_members = set(members)

    assert actual_members == expected_members, (
        f"Tarball contents do not match expected.\n"
        f"Expected: {expected_members}\n"
        f"Got: {actual_members}\n"
        f"Make sure to not include the configs/ directory structure."
    )
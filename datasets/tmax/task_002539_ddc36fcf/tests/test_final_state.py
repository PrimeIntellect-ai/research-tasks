# test_final_state.py

import os
import tarfile
import hashlib
import pytest

def test_manifest_exists_and_format():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in manifest.txt, but got {len(lines)}"

    # Expected content of the files after replacement
    expected_files = {
        "etc/app1/net.conf": "[network]\nbind_addr=192.168.1.100\nport=8080\n",
        "etc/app2/settings.conf": "debug=true\nbind_addr=10.0.0.5\ntimeout=30\n",
        "var/lib/app3/data.conf": "path=/var/data\nbind_addr=127.0.0.1\n"
    }

    expected_hashes = {}
    for path, content in expected_files.items():
        expected_hashes[path] = hashlib.sha256(content.encode('utf-8')).hexdigest()

    actual_manifest = {}
    for line in lines:
        parts = line.split()
        assert len(parts) == 2, f"Invalid manifest line format: '{line}'"
        checksum, path = parts
        actual_manifest[path] = checksum

    for path, expected_hash in expected_hashes.items():
        assert path in actual_manifest, f"Expected path {path} not found in manifest"
        assert actual_manifest[path] == expected_hash, f"Checksum mismatch for {path}. Expected {expected_hash}, got {actual_manifest[path]}"

def test_tarball_exists_and_contents():
    tarball_path = "/home/user/config_backup.tar.gz"
    assert os.path.isfile(tarball_path), f"Tarball missing at {tarball_path}"

    assert tarfile.is_tarfile(tarball_path), f"File {tarball_path} is not a valid tar archive"

    with tarfile.open(tarball_path, "r:gz") as tar:
        names = tar.getnames()

    expected_paths = [
        "etc/app1/net.conf",
        "etc/app2/settings.conf",
        "var/lib/app3/data.conf"
    ]

    # Check that expected paths are in the tarball (they might be prefixed with './' or just 'etc/...')
    # We will normalize names by stripping leading './'
    normalized_names = [name[2:] if name.startswith("./") else name for name in names]

    for path in expected_paths:
        assert path in normalized_names, f"Expected file {path} not found in tarball. Found: {normalized_names}"

def test_c_source_code_exists():
    c_file_path = "/home/user/config_archiver.c"
    assert os.path.isfile(c_file_path), f"C source file missing at {c_file_path}"

    with open(c_file_path, "r") as f:
        content = f.read()

    assert "openssl" in content.lower() or "crypto" in content.lower(), "C source file does not appear to use OpenSSL/libcrypto"

def test_sys_root_intact():
    expected_files = {
        "/home/user/sys_root/etc/app1/net.conf": "server_ip=192.168.1.100",
        "/home/user/sys_root/etc/app2/settings.conf": "server_ip=10.0.0.5",
        "/home/user/sys_root/var/lib/app3/data.conf": "server_ip=127.0.0.1",
        "/home/user/sys_root/opt/ignored/skip.conf": "server_ip=0.0.0.0",
    }
    for file_path, expected_content in expected_files.items():
        assert os.path.isfile(file_path), f"Original file {file_path} is missing"
        with open(file_path, "r") as f:
            content = f.read()
            assert expected_content in content, f"Original file {file_path} was modified. Expected '{expected_content}'"
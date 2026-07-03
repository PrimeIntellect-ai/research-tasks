# test_final_state.py

import os
import hashlib
import tarfile
import pytest

MANIFEST_PATH = "/home/user/change_manifest.txt"
ARCHIVE_PATH = "/home/user/update.tar.gz"
CURRENT_CONFIGS = "/home/user/current_configs"

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def test_manifest_exists_and_correct():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"

    expected_files = {
        "./app/logging.conf": "NEW",
        "./network/routing.conf": "NEW",
        "./network/sysctl.conf": "MODIFIED"
    }

    expected_lines = []
    for rel_path in sorted(expected_files.keys()):
        status = expected_files[rel_path]
        abs_path = os.path.join(CURRENT_CONFIGS, rel_path[2:])
        assert os.path.exists(abs_path), f"Expected file {abs_path} missing from current_configs"
        checksum = get_sha256(abs_path)
        expected_lines.append(f"[{status}] {rel_path} {checksum}")

    with open(MANIFEST_PATH, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Manifest contents are incorrect.\nExpected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_archive_exists_and_correct():
    assert os.path.exists(ARCHIVE_PATH), f"Update archive missing at {ARCHIVE_PATH}"
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"File {ARCHIVE_PATH} is not a valid tar archive"

    expected_members = {
        "app/logging.conf",
        "network/routing.conf",
        "network/sysctl.conf"
    }

    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        members = tar.getmembers()

        # Check that only expected files are in the archive
        actual_files = {m.name.lstrip("./") for m in members if m.isfile()}
        assert actual_files == expected_members, (
            f"Archive contains incorrect files.\nExpected: {expected_members}\nActual: {actual_files}"
        )

        # Check that symlinks were dereferenced (no symlinks in archive)
        symlinks = [m.name for m in members if m.issym() or m.islnk()]
        assert not symlinks, f"Archive must not contain symlinks, but found: {symlinks}"

        # Verify contents of the archived files match the current_configs
        for member in members:
            if member.isfile():
                rel_name = member.name.lstrip("./")
                abs_path = os.path.join(CURRENT_CONFIGS, rel_name)

                f = tar.extractfile(member)
                archived_content = f.read()

                with open(abs_path, 'rb') as src:
                    expected_content = src.read()

                assert archived_content == expected_content, f"Content of {rel_name} in archive does not match {abs_path}"
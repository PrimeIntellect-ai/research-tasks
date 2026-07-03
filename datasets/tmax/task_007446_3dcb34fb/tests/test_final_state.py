# test_final_state.py

import os
import csv
import tarfile
import hashlib
import re
import tempfile
import pytest

MANIFEST_PATH = "/home/user/manifest.csv"
TARBALL_PATH = "/home/user/safe_backup.tar.gz"
BACKUP_PLAN_PATH = "/home/user/server_data/backup_plan.json"

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_manifest_exists_and_format():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing: {MANIFEST_PATH}"

    with open(MANIFEST_PATH, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["file_path", "sha256_hash"], "Manifest header is incorrect"

        rows = list(reader)
        assert len(rows) == 3, "Manifest should contain exactly 3 entries"

        # Check sorting by file_path
        file_paths = [row[0] for row in rows]
        assert file_paths == sorted(file_paths), "Manifest rows are not sorted alphabetically by file_path"

        expected_files = ["conf/settings.xml", "logs/access.csv", "logs/system.log"]
        assert set(file_paths) == set(expected_files), "Manifest contains incorrect file paths"

def test_tarball_exists_and_contents():
    assert os.path.isfile(TARBALL_PATH), f"Tarball missing: {TARBALL_PATH}"
    assert tarfile.is_tarfile(TARBALL_PATH), f"{TARBALL_PATH} is not a valid tar file"

    with tarfile.open(TARBALL_PATH, "r:gz") as tar:
        members = tar.getnames()

        # Validate no absolute paths or parent directory inclusion
        for member in members:
            assert not member.startswith("/"), f"Tarball contains absolute paths: {member}"
            assert not member.startswith("server_data"), f"Tarball contains parent directory 'server_data': {member}"

        # Filter out directories
        file_members = [m.name for m in tar.getmembers() if m.isfile()]

        expected_files = {"conf/settings.xml", "logs/access.csv", "logs/system.log"}
        assert set(file_members) == expected_files, f"Tarball contains incorrect files. Found: {file_members}"

        assert "conf/secrets.txt" not in file_members, "Tarball incorrectly contains conf/secrets.txt"

def test_extraction_redaction_and_hashes():
    assert os.path.isfile(MANIFEST_PATH), "Manifest missing"
    assert os.path.isfile(TARBALL_PATH), "Tarball missing"

    # Read manifest hashes
    manifest_hashes = {}
    with open(MANIFEST_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            manifest_hashes[row["file_path"]] = row["sha256_hash"]

    ipv4_regex = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(TARBALL_PATH, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        for file_path, expected_hash in manifest_hashes.items():
            extracted_file = os.path.join(tmpdir, file_path)
            assert os.path.isfile(extracted_file), f"File {file_path} missing from extracted tarball"

            # Check hash matches manifest
            actual_hash = get_sha256(extracted_file)
            assert actual_hash == expected_hash, f"Hash mismatch for {file_path}. Manifest: {expected_hash}, Actual: {actual_hash}"

            # Check redaction
            with open(extracted_file, "r") as f:
                content = f.read()

            if "access.csv" in file_path or "system.log" in file_path:
                assert "[REDACTED]" in content, f"Expected [REDACTED] string not found in {file_path}"
                matches = ipv4_regex.findall(content)
                assert not matches, f"Found unredacted IPv4 addresses in {file_path}: {matches}"
            elif "settings.xml" in file_path:
                assert "[REDACTED]" not in content, f"File {file_path} should not be redacted"
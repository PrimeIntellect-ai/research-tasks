# test_final_state.py
import os
import json
import tarfile
import hashlib
import pytest

BASE_DIR = "/home/user/artifact_dump"
SECURITY_LOG = "/home/user/security_logs.txt"
MANIFEST_FILE = "/home/user/manifest.json"
ARCHIVE_FILE = "/home/user/clean_artifacts.tar.gz"

def get_blacklisted_hashes():
    blacklist = set()
    if os.path.exists(SECURITY_LOG):
        with open(SECURITY_LOG, "r") as f:
            for line in f:
                if "[ERROR] Corrupt file detected - BLACKLIST_HASH:" in line:
                    parts = line.strip().split("BLACKLIST_HASH:")
                    if len(parts) == 2:
                        blacklist.add(parts[1].strip())
    return blacklist

def get_expected_artifacts():
    blacklist = get_blacklisted_hashes()
    expected = {}
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".bin"):
                path = os.path.join(root, file)
                if os.path.islink(path):
                    continue
                with open(path, "rb") as f:
                    content = f.read()
                file_hash = hashlib.sha256(content).hexdigest()
                if file_hash in blacklist:
                    continue
                version = content[:16].decode('ascii', errors='ignore').rstrip('-')
                rel_path = os.path.relpath(path, BASE_DIR)
                expected[file_hash] = {
                    "version": version,
                    "path": rel_path
                }
    return expected

def test_manifest_exists_and_correct():
    assert os.path.isfile(MANIFEST_FILE), f"Manifest file missing: {MANIFEST_FILE}"

    with open(MANIFEST_FILE, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    expected = get_expected_artifacts()

    assert set(manifest.keys()) == set(expected.keys()), f"Manifest keys (hashes) do not match expected valid artifacts. Expected: {list(expected.keys())}, Got: {list(manifest.keys())}"

    for h, data in expected.items():
        assert manifest[h]["version"] == data["version"], f"Version mismatch for hash {h}. Expected {data['version']}, got {manifest[h]['version']}"
        manifest_path = manifest[h]["path"]
        abs_manifest_path = os.path.join(BASE_DIR, manifest_path)
        assert os.path.exists(abs_manifest_path), f"Path in manifest does not exist: {manifest_path}"
        assert abs_manifest_path.endswith(data["path"].split('/')[-1]), f"Path in manifest does not seem to point to the correct file: {manifest_path}"

def test_archive_exists_and_correct():
    assert os.path.isfile(ARCHIVE_FILE), f"Archive file missing: {ARCHIVE_FILE}"
    assert tarfile.is_tarfile(ARCHIVE_FILE), "Archive is not a valid tar file"

    expected = get_expected_artifacts()
    expected_filenames = {f"{h}.bin" for h in expected.keys()}

    with tarfile.open(ARCHIVE_FILE, "r:gz") as tar:
        members = tar.getmembers()

        for member in members:
            assert member.isfile(), f"Archive contains non-file member: {member.name}"
            assert "/" not in member.name and "\\" not in member.name, f"Archive contains nested file (not at root): {member.name}"

        actual_filenames = {member.name for member in members}
        assert actual_filenames == expected_filenames, f"Archive contents mismatch. Expected {expected_filenames}, got {actual_filenames}"

        for h in expected.keys():
            filename = f"{h}.bin"
            f = tar.extractfile(filename)
            assert f is not None, f"Could not extract {filename} from archive"
            content = f.read()
            actual_hash = hashlib.sha256(content).hexdigest()
            assert actual_hash == h, f"Hash mismatch for file {filename} in archive. File contents do not match the expected hash."
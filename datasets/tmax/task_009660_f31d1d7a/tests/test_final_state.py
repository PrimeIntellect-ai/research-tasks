# test_final_state.py

import os
import json
import tarfile
import hashlib
import tempfile
import re
import pytest

FINAL_TAR = "/home/user/final_backup.tar"
SCRIPT_PATH = "/home/user/safe_backup.py"

def get_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def test_final_backup_exists_and_extracts():
    assert os.path.isfile(FINAL_TAR), f"Final backup archive {FINAL_TAR} does not exist."
    assert tarfile.is_tarfile(FINAL_TAR), f"{FINAL_TAR} is not a valid tar file."

def test_manifest_and_archives_in_tarball():
    assert os.path.isfile(FINAL_TAR), "Final tarball missing."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(FINAL_TAR, "r") as tar:
            tar.extractall(path=tmpdir)

        # Look for manifest.json
        manifest_path = os.path.join(tmpdir, "manifest.json")
        assert os.path.isfile(manifest_path), "manifest.json is missing from the final tarball."

        # Check nested archives
        assert os.path.isfile(os.path.join(tmpdir, "dirA.tar.gz")), "dirA.tar.gz is missing from the tarball."
        assert os.path.isfile(os.path.join(tmpdir, "dirB.tar.gz")), "dirB.tar.gz is missing from the tarball."

        # Validate manifest content
        with open(manifest_path, "r") as f:
            try:
                manifest = json.load(f)
            except json.JSONDecodeError:
                pytest.fail("manifest.json is not valid JSON.")

        expected_hashes = {
            "dirA/fileA.txt": get_sha256(b"data_A\n"),
            "dirB/fileB.txt": get_sha256(b"data_B\n"),
            "root.txt": get_sha256(b"root_file\n"),
            "dirA/valid_link.txt": get_sha256(b"root_file\n")
        }

        for path, expected_hash in expected_hashes.items():
            assert path in manifest, f"Expected path {path} missing in manifest.json"
            assert manifest[path] == expected_hash, f"Hash mismatch for {path}. Expected {expected_hash}, got {manifest[path]}"

        # Check that no infinite loop paths are present
        for path in manifest.keys():
            assert "loop_to_B" not in path, f"Infinite loop path found in manifest: {path}"
            assert "loop_to_A" not in path, f"Infinite loop path found in manifest: {path}"

def test_script_uses_atomic_write():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    # Check for temporary file usage and rename/replace/move
    has_tmp = ".tmp" in content or "manifest.json.tmp" in content
    has_atomic_op = re.search(r'(os\.rename|os\.replace|shutil\.move)\s*\(', content)

    assert has_tmp and has_atomic_op, "Script does not appear to use an atomic write pattern (writing to a .tmp file and renaming/replacing)."
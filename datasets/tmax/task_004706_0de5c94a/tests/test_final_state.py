# test_final_state.py

import os
import json
import hashlib
import tarfile

def compute_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_manifest_v2_generated_correctly():
    manifest_path = "/home/user/backups/manifest_v2.json"
    assert os.path.isfile(manifest_path), f"Manifest file missing: {manifest_path}"

    with open(manifest_path, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Manifest file {manifest_path} is not valid JSON."

    repo_dir = "/home/user/repo"
    expected_files = [
        "bin/app_v1",
        "bin/app_v2",
        "lib/libcore.so",
        "lib/libold.so"
    ]

    unexpected_files = [
        "bin/cache.tmp",
        "docs/readme.txt"
    ]

    for f in expected_files:
        assert f in manifest, f"Expected file {f} missing from manifest_v2.json"
        actual_path = os.path.join(repo_dir, f)
        expected_hash = compute_sha256(actual_path)
        assert manifest[f] == expected_hash, f"Hash mismatch for {f} in manifest_v2.json"

    for f in unexpected_files:
        assert f not in manifest, f"File {f} should not be included in manifest_v2.json (check include_dirs and exclude_patterns)"

    # Ensure no extra files are present
    for f in manifest.keys():
        assert f in expected_files, f"Unexpected file {f} found in manifest_v2.json"

def test_backup_summary_generated_correctly():
    summary_path = "/home/user/backups/backup_summary.txt"
    assert os.path.isfile(summary_path), f"Summary file missing: {summary_path}"

    with open(summary_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "MODIFIED: lib/libcore.so",
        "NEW: bin/app_v2"
    ]

    # The prompt requires them to be sorted alphabetically by file path.
    # "bin/app_v2" comes before "lib/libcore.so"
    expected_sorted = [
        "NEW: bin/app_v2",
        "MODIFIED: lib/libcore.so"
    ]

    assert lines == expected_sorted, f"Backup summary content or sorting is incorrect. Expected {expected_sorted}, got {lines}"

def test_incremental_tarball_generated_correctly():
    tarball_path = "/home/user/backups/incremental_v2.tar.gz"
    assert os.path.isfile(tarball_path), f"Tarball file missing: {tarball_path}"

    assert tarfile.is_tarfile(tarball_path), f"File {tarball_path} is not a valid tar archive"

    with tarfile.open(tarball_path, 'r:gz') as tar:
        members = tar.getnames()

    # We only care about file entries, but tarballs might include directory entries.
    # Let's filter out directories if they exist, or just check that the required files are present and no unexpected files are present.
    expected_files = {
        "bin/app_v2",
        "lib/libcore.so"
    }

    unexpected_files = {
        "bin/app_v1",
        "lib/libold.so",
        "bin/cache.tmp",
        "docs/readme.txt"
    }

    # Clean up member names (sometimes they might have a leading ./)
    cleaned_members = {m.lstrip('./') for m in members}

    for f in expected_files:
        assert f in cleaned_members, f"Expected file {f} missing from {tarball_path}"

    for f in unexpected_files:
        assert f not in cleaned_members, f"Unexpected file {f} found in {tarball_path}"

    # Ensure no absolute paths
    for m in members:
        assert not m.startswith("/"), f"Tarball contains absolute path: {m}. Paths must be relative to /home/user/repo/"
        assert not m.startswith("home/user/repo"), f"Tarball contains full path structure: {m}. Paths must be relative to /home/user/repo/"
# test_final_state.py

import os
import hashlib
import tarfile
import pytest

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def test_backup_manager_script_exists():
    script_path = "/home/user/backup_manager.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

def test_renamed_files():
    target_dir = "/home/user/raw_data"
    assert os.path.isdir(target_dir), f"{target_dir} does not exist."

    expected_files = {
        "Financial_Report_2023.csv": "Q1 Revenue: $1000\n",
        "Meeting_notes.txt": "Discussed architecture.\n",
        "daily_log.txt": "All systems operational.\n"
    }

    actual_files = os.listdir(target_dir)
    assert set(actual_files) == set(expected_files.keys()), f"Files in {target_dir} do not match expected renamed files. Found: {actual_files}"

    for filename, content in expected_files.items():
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "r") as f:
            actual_content = f.read()
        assert actual_content == content, f"Content of {filename} was altered."

def test_manifest():
    manifest_path = "/home/user/manifest.sha256"
    assert os.path.isfile(manifest_path), f"{manifest_path} does not exist."

    expected_hashes = {
        "Financial_Report_2023.csv": "10e08f8dc1c7ef5ab7492cda19dd8880fc4aef2b8eec1daab9a06cc5b3ebcfb9",
        "Meeting_notes.txt": "ea6fb59b151cb829cb8c5a2c2864caef20c5dbcd6c6dfbf46e01a8ed291a27e7",
        "daily_log.txt": "5ce83344a04d6e902b4bc65839b207eb3d3bd088e8b0fb6b4f7626fc965f37bc"
    }

    with open(manifest_path, "r") as f:
        manifest_lines = f.read().strip().splitlines()

    assert len(manifest_lines) == 3, f"Manifest should contain exactly 3 lines, found {len(manifest_lines)}."

    manifest_dict = {}
    for line in manifest_lines:
        parts = line.strip().split()
        assert len(parts) >= 2, f"Invalid manifest line format: {line}"
        hash_val = parts[0]
        # Get base filename from path
        filename = os.path.basename(parts[1])
        manifest_dict[filename] = hash_val

    for filename, expected_hash in expected_hashes.items():
        assert filename in manifest_dict, f"{filename} missing from manifest."
        assert manifest_dict[filename] == expected_hash, f"Hash mismatch for {filename} in manifest."

def test_archive():
    archive_path = "/home/user/archive.tar.gz"
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()

    # Check if the expected files are in the archive
    # They should be inside raw_data directory
    expected_basenames = ["Financial_Report_2023.csv", "Meeting_notes.txt", "daily_log.txt"]

    found_files = 0
    for name in names:
        basename = os.path.basename(name)
        if basename in expected_basenames:
            found_files += 1

    assert found_files == 3, f"Archive does not contain all expected files. Found names: {names}"

def test_backup_log():
    log_path = "/home/user/backup_log.txt"
    archive_path = "/home/user/archive.tar.gz"

    assert os.path.isfile(log_path), f"{log_path} does not exist."
    assert os.path.isfile(archive_path), "Archive must exist to test backup log."

    actual_archive_hash = get_sha256(archive_path)

    with open(log_path, "r") as f:
        log_content = f.read().strip().splitlines()

    assert len(log_content) == 2, f"Backup log should have exactly 2 lines, found {len(log_content)}."

    assert log_content[0].startswith("Archive Checksum: "), "First line of backup log must start with 'Archive Checksum: '"
    logged_hash = log_content[0].replace("Archive Checksum: ", "").strip()
    assert logged_hash == actual_archive_hash, f"Logged archive checksum ({logged_hash}) does not match actual checksum ({actual_archive_hash})."

    assert log_content[1].startswith("Files Archived: "), "Second line of backup log must start with 'Files Archived: '"
    logged_count = log_content[1].replace("Files Archived: ", "").strip()
    assert logged_count == "3", f"Logged files archived count should be 3, found '{logged_count}'."
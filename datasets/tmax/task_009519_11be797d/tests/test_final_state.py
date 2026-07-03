# test_final_state.py

import os
import stat
import tarfile
import hashlib
import pytest

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def test_backup_tool_exists_and_executable():
    assert os.path.isfile('/home/user/backup_tool.c'), "Source file /home/user/backup_tool.c does not exist."
    assert os.path.isfile('/home/user/backup_tool'), "Compiled binary /home/user/backup_tool does not exist."
    st = os.stat('/home/user/backup_tool')
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), "Compiled binary /home/user/backup_tool is not executable."

def test_backup_directory_contains_renamed_files():
    backup_dir = '/home/user/backup'
    assert os.path.isdir(backup_dir), f"Directory {backup_dir} does not exist."

    expected_files = [
        'img_test.png',
        'doc_info.txt',
        'src_app.c',
        'file.bin'
    ]

    for f in expected_files:
        filepath = os.path.join(backup_dir, f)
        assert os.path.isfile(filepath), f"Expected backup file {filepath} does not exist."

def test_new_manifest_format_and_content():
    manifest_path = '/home/user/new_manifest.txt'
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    with open(manifest_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in manifest, found {len(lines)}."

    raw_data_dir = '/home/user/raw_data'
    expected_entries = {}
    for orig_name in ['test.png', 'info.txt', 'app.c', 'file.bin']:
        raw_path = os.path.join(raw_data_dir, orig_name)
        if os.path.isfile(raw_path):
            expected_entries[orig_name] = get_sha256(raw_path)

    found_files = set()
    for line in lines:
        parts = line.split('|')
        assert len(parts) == 3, f"Manifest line '{line}' does not match format original_filename|mtime|sha256sum."
        orig_name, mtime, sha256sum = parts
        found_files.add(orig_name)

        assert orig_name in expected_entries, f"Unexpected file {orig_name} in manifest."
        assert sha256sum == expected_entries[orig_name], f"Checksum mismatch for {orig_name}."
        assert mtime.isdigit() or (mtime.replace('.','',1).isdigit()), f"mtime '{mtime}' is not a valid number."

    assert found_files == set(expected_entries.keys()), "Not all original files were found in the manifest."

def test_backup_archive_exists_and_valid():
    archive_path = '/home/user/backup_archive.tar.gz'
    assert os.path.isfile(archive_path), f"Archive file {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, 'r:gz') as tar:
        names = tar.getnames()
        # The tarball might contain the directory itself or just the files.
        # We just check if the basenames of the expected files are present.
        basenames = [os.path.basename(name) for name in names]

        expected_files = [
            'img_test.png',
            'doc_info.txt',
            'src_app.c',
            'file.bin'
        ]

        for f in expected_files:
            assert f in basenames, f"Expected file {f} not found in the tarball."
# test_final_state.py

import os
import json
import hashlib
import pytest

def test_go_source_code_exists_and_atomic_ops():
    go_file = "/home/user/config_manager.go"
    assert os.path.isfile(go_file), f"Go source file missing at {go_file}"

    with open(go_file, "r") as f:
        content = f.read()

    assert "os.Rename" in content, "Go code must use os.Rename for atomic operations"
    assert "os.Symlink" in content, "Go code must use os.Symlink for creating the symlink"

def test_snapshot_directory_exists():
    snapshot_dir = "/home/user/snapshots/my_run"
    assert os.path.isdir(snapshot_dir), f"Snapshot directory missing at {snapshot_dir}"

def test_current_symlink():
    symlink_path = "/home/user/snapshots/current"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"

    target = os.path.realpath(symlink_path)
    expected_target = os.path.realpath("/home/user/snapshots/my_run")
    assert target == expected_target, f"Symlink points to {target}, expected {expected_target}"

def test_hard_links():
    snapshot_dir = "/home/user/snapshots/my_run"

    expected_links = {
        "app1_db.conf": "/home/user/etc_mock/app1/db.conf",
        "nginx_nginx.conf": "/home/user/etc_mock/nginx/nginx.conf"
    }

    for snap_file, orig_file in expected_links.items():
        snap_path = os.path.join(snapshot_dir, snap_file)
        assert os.path.isfile(snap_path), f"Hard link missing: {snap_path}"

        orig_stat = os.stat(orig_file)
        snap_stat = os.stat(snap_path)

        assert orig_stat.st_ino == snap_stat.st_ino, f"File {snap_path} is not a hard link to {orig_file} (inodes differ)"
        assert orig_stat.st_dev == snap_stat.st_dev, f"File {snap_path} and {orig_file} are on different devices"

def test_filtered_files_not_present():
    snapshot_dir = "/home/user/snapshots/my_run"

    unexpected_files = [
        "app1_old.conf",
        "old_root.conf",
        "nginx_not_a_conf.txt",
        "not_a_conf.txt"
    ]

    for f in unexpected_files:
        path = os.path.join(snapshot_dir, f)
        assert not os.path.exists(path), f"Filtered file should not be in snapshot: {path}"

def test_manifest_json():
    manifest_path = "/home/user/snapshots/my_run/manifest.json"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest file is not valid JSON")

    expected_files = [
        "/home/user/etc_mock/app1/db.conf",
        "/home/user/etc_mock/nginx/nginx.conf"
    ]

    assert len(manifest) == len(expected_files), f"Manifest should contain exactly {len(expected_files)} keys"

    for orig_file in expected_files:
        assert orig_file in manifest, f"Manifest is missing key for {orig_file}"

        # Calculate expected checksum
        with open(orig_file, "rb") as f:
            file_bytes = f.read()
            expected_checksum = hashlib.sha256(file_bytes).hexdigest()

        assert manifest[orig_file] == expected_checksum, f"Checksum mismatch for {orig_file}"
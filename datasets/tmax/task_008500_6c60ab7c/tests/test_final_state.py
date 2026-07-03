# test_final_state.py

import os
import json
import tarfile
import hashlib
import configparser
import csv
import io
import pytest

def get_expected_targets():
    config_path = "/home/user/backups/storage_policy.ini"
    assert os.path.isfile(config_path), f"Missing {config_path}"
    config = configparser.ConfigParser()
    config.read(config_path)
    assert "Policy" in config, "Missing [Policy] section in storage_policy.ini"
    assert "target_dirs" in config["Policy"], "Missing target_dirs in [Policy]"
    targets = [d.strip() for d in config["Policy"]["target_dirs"].split(",") if d.strip()]
    return targets

def compute_expected_reclaimable_bytes():
    targets = get_expected_targets()
    base_dir = "/home/user/backups"
    total_bytes = 0

    for target in targets:
        tar_path = os.path.join(base_dir, target, "data.tar.gz")
        assert os.path.isfile(tar_path), f"Missing archive {tar_path}"

        with tarfile.open(tar_path, "r:gz") as tar:
            try:
                member = tar.getmember("usage.csv")
            except KeyError:
                continue

            f = tar.extractfile(member)
            if f is None:
                continue

            content = f.read().decode('utf-8')
            reader = csv.reader(io.StringIO(content))
            for row in reader:
                if len(row) < 4:
                    continue
                filename, filetype, size_in_bytes, last_accessed_days_ago = row
                try:
                    size = int(size_in_bytes)
                    days = int(last_accessed_days_ago)
                except ValueError:
                    continue

                if days > 90 and filetype in ("tmp", "cache"):
                    total_bytes += size

    return total_bytes

def test_analyzer_c_exists():
    assert os.path.isfile("/home/user/analyzer.c"), "The C source file /home/user/analyzer.c is missing."

def test_reclaim_manifest_json():
    manifest_path = "/home/user/reclaim_manifest.json"
    assert os.path.isfile(manifest_path), f"Missing {manifest_path}"

    with open(manifest_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{manifest_path} is not valid JSON.")

    assert "reclaimable_bytes" in data, f"Key 'reclaimable_bytes' missing in {manifest_path}"

    expected_bytes = compute_expected_reclaimable_bytes()
    assert data["reclaimable_bytes"] == expected_bytes, \
        f"Expected reclaimable_bytes to be {expected_bytes}, but got {data['reclaimable_bytes']}"

def test_reclaim_data_tar_gz():
    tar_path = "/home/user/reclaim_data.tar.gz"
    assert os.path.isfile(tar_path), f"Missing {tar_path}"

    expected_targets = get_expected_targets()
    expected_members = set(f"{target}/usage.csv" for target in expected_targets)

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            members = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"{tar_path} is not a valid gzip-compressed tar archive.")

    actual_files = set(m for m in members if not m.endswith('/'))

    assert actual_files == expected_members, \
        f"Archive contents mismatch. Expected files: {expected_members}, Found: {actual_files}"

def test_reclaim_data_sha256():
    tar_path = "/home/user/reclaim_data.tar.gz"
    sha_path = "/home/user/reclaim_data.sha256"

    assert os.path.isfile(tar_path), f"Missing {tar_path} needed for checksum verification."
    assert os.path.isfile(sha_path), f"Missing {sha_path}"

    # Compute actual SHA256 of the tarball
    hasher = hashlib.sha256()
    with open(tar_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    expected_hash = hasher.hexdigest()

    with open(sha_path, "r") as f:
        content = f.read().strip()

    # The output of sha256sum usually looks like: "<hash>  <filename>"
    # We just need to check if the hash is present as the first token
    actual_hash = content.split()[0] if content else ""

    assert actual_hash == expected_hash, \
        f"Checksum mismatch. Expected {expected_hash}, but found {actual_hash} in {sha_path}"
# test_final_state.py

import os
import hashlib
import tarfile
import csv
import pytest

CONFIG_DIR = "/home/user/config_data"
MANIFEST_PATH = "/home/user/output/manifest.csv"
TARBALL_PATH = "/home/user/output/active_configs.tar.gz"

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_manifest_content():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing at {MANIFEST_PATH}"

    expected_app1_sha = get_sha256(os.path.join(CONFIG_DIR, "app1.json"))
    expected_app3_sha = get_sha256(os.path.join(CONFIG_DIR, "app3.json"))

    with open(MANIFEST_PATH, "r", newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 3, f"Manifest should have exactly 3 rows (header + 2 active files), but found {len(rows)}."

    assert rows[0] == ["filename", "version", "sha256"], f"Incorrect header in manifest: {rows[0]}"

    assert rows[1] == ["app1.json", "1.4.2", expected_app1_sha], f"Incorrect row for app1.json: {rows[1]}"
    assert rows[2] == ["app3.json", "9.4.1", expected_app3_sha], f"Incorrect row for app3.json: {rows[2]}"

def test_tarball_content():
    assert os.path.isfile(TARBALL_PATH), f"Tarball missing at {TARBALL_PATH}"
    assert tarfile.is_tarfile(TARBALL_PATH), f"File {TARBALL_PATH} is not a valid tar archive"

    with tarfile.open(TARBALL_PATH, "r:gz") as tar:
        members = tar.getnames()

    expected_members = ["app1.json", "app3.json"]
    assert sorted(members) == expected_members, f"Tarball must contain exactly {expected_members} at the root, but found {members}"
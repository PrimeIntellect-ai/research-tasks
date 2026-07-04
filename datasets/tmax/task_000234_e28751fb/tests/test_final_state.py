# test_final_state.py

import os
import json
import hashlib
import tarfile
import tempfile
import glob
import pytest

CONFIGS_DIR = "/home/user/configs"
MANIFEST_PATH = "/home/user/configs/manifest.json"
TARBALL_PATH = "/home/user/configs_backup.tar.gz"
COLD_STORAGE_DIR = "/home/user/cold_storage"

EXPECTED_CONFIGS = {
    "web_01/1690000000.conf": "server {\n  listen 80;\n  server_name example.com;\n}\n",
    "db_master/1690000500.conf": "max_connections=500\nshared_buffers=2GB\n",
    "cache_node/1690001000.conf": "".join([f"bind 192.168.1.{i}\n" for i in range(50)])
}

def get_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def test_extracted_configs():
    for rel_path, expected_content in EXPECTED_CONFIGS.items():
        full_path = os.path.join(CONFIGS_DIR, rel_path)
        assert os.path.isfile(full_path), f"Expected configuration file missing: {full_path}"
        with open(full_path, "r") as f:
            content = f.read()
        assert content == expected_content, f"Content mismatch in {full_path}"

def test_manifest_json():
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file missing: {MANIFEST_PATH}"
    with open(MANIFEST_PATH, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    for rel_path, expected_content in EXPECTED_CONFIGS.items():
        assert rel_path in manifest, f"Manifest missing entry for {rel_path}"
        expected_hash = get_sha256(expected_content)
        assert manifest[rel_path] == expected_hash, f"Hash mismatch in manifest for {rel_path}"

def test_tarball_exists_and_valid():
    assert os.path.isfile(TARBALL_PATH), f"Tarball missing: {TARBALL_PATH}"
    assert tarfile.is_tarfile(TARBALL_PATH), f"File is not a valid tarball: {TARBALL_PATH}"

    with tarfile.open(TARBALL_PATH, "r:gz") as tar:
        names = tar.getnames()
        # Check that the root directory is 'configs'
        assert any(name == "configs" or name.startswith("configs/") for name in names), "Tarball must have 'configs' as the root directory"

        for rel_path in EXPECTED_CONFIGS.keys():
            expected_tar_path = f"configs/{rel_path}"
            assert expected_tar_path in names, f"Tarball missing file: {expected_tar_path}"

def test_chunks_and_reassembly():
    assert os.path.isdir(COLD_STORAGE_DIR), f"Cold storage directory missing: {COLD_STORAGE_DIR}"

    chunks = sorted(glob.glob(os.path.join(COLD_STORAGE_DIR, "backup.part_*")))
    assert len(chunks) > 0, "No backup chunks found in cold storage"

    # Check that all chunks except the last one are exactly 1024 bytes
    for chunk in chunks[:-1]:
        assert os.path.getsize(chunk) == 1024, f"Chunk {chunk} is not exactly 1024 bytes"

    # Reassemble and compare with original tarball
    reassembled_content = bytearray()
    for chunk in chunks:
        with open(chunk, "rb") as f:
            reassembled_content.extend(f.read())

    with open(TARBALL_PATH, "rb") as f:
        original_content = f.read()

    assert reassembled_content == original_content, "Reassembled chunks do not match the original tarball exactly"
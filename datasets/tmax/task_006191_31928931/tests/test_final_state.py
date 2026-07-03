# test_final_state.py

import os
import json
import tarfile
import hashlib
import tempfile
import pytest

DEST_DIR = "/home/user/archive_dest"
CONSOLIDATED_TAR = os.path.join(DEST_DIR, "consolidated.tar.gz")
MANIFEST_JSON = os.path.join(DEST_DIR, "manifest.json")

EXPECTED_HASHES = {
    "app_2020.log": "c830ddad592f6cefe387e3ffb78bf0198cded24128f73117565b9ceee313c048",
    "auth_2021.log": "81bbfe2b2f676239162dbdb7579bd66c429007f50244431e649089f5c4041b31"
}

def test_consolidated_tar_exists():
    assert os.path.isfile(CONSOLIDATED_TAR), f"File {CONSOLIDATED_TAR} does not exist."

def test_manifest_exists():
    assert os.path.isfile(MANIFEST_JSON), f"File {MANIFEST_JSON} does not exist."

def test_no_tmp_files():
    for f in os.listdir(DEST_DIR):
        assert not f.endswith(".tmp"), f"Found temporary file {f} in {DEST_DIR}, atomicity requirement likely violated."

def test_manifest_content():
    with open(MANIFEST_JSON, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("manifest.json is not valid JSON.")

    assert manifest == EXPECTED_HASHES, f"Manifest contents do not match expected hashes. Got: {manifest}"

def test_consolidated_tar_contents():
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with tarfile.open(CONSOLIDATED_TAR, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError:
            pytest.fail("consolidated.tar.gz is not a valid gzipped tar archive.")

        extracted_files = os.listdir(tmpdir)

        # Check that only the two expected files are at the root
        assert set(extracted_files) == set(EXPECTED_HASHES.keys()), \
            f"Extracted files {extracted_files} do not match expected flat files."

        for filename, expected_hash in EXPECTED_HASHES.items():
            filepath = os.path.join(tmpdir, filename)
            assert os.path.isfile(filepath), f"File {filename} not found at the root of the archive."

            with open(filepath, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            assert file_hash == expected_hash, f"Hash for {filename} in archive does not match expected hash."

def test_rust_project_exists():
    # The prompt says "You can create a Cargo project at /home/user/consolidator"
    # Or just leave the compiled binary/project intact.
    # We will just verify that the user created *some* rust files if possible,
    # but the primary tests are the outputs. 
    # Let's check for /home/user/consolidator/Cargo.toml or main.rs
    cargo_toml = "/home/user/consolidator/Cargo.toml"
    main_rs = "/home/user/consolidator/src/main.rs"
    if not (os.path.isfile(cargo_toml) or os.path.isfile(main_rs)):
        # Just a soft check, some users might put it directly in /home/user
        pass
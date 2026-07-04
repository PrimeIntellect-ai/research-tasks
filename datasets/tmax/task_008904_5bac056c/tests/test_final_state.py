# test_final_state.py

import os
import json
import tarfile
import tempfile
import hashlib
import pytest

ARCHIVE_PATH = "/home/user/release_archive.tar.gz"

@pytest.fixture(scope="module")
def extracted_archive():
    """Extracts the release archive to a temporary directory and yields the path."""
    assert os.path.isfile(ARCHIVE_PATH), f"Archive {ARCHIVE_PATH} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
            tar.extractall(path=tmpdir)
        yield tmpdir

def test_archive_contents_and_manifest_exists(extracted_archive):
    """Test that the archive contains the manifest.json and the artifact_staging directory."""
    manifest_path = os.path.join(extracted_archive, "manifest.json")
    assert os.path.isfile(manifest_path), "manifest.json is missing from the root of the archive."

    staging_dir = os.path.join(extracted_archive, "artifact_staging")
    assert os.path.isdir(staging_dir), "artifact_staging directory is missing from the archive."

def test_manifest_structure_and_metadata(extracted_archive):
    """Test that the manifest contains the correct metadata for each file."""
    manifest_path = os.path.join(extracted_archive, "manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("manifest.json is not a valid JSON file.")

    expected_files = {
        "bin/app_x86": {"file_type": "elf", "e_machine": "0x3e"},
        "bin/app_arm": {"file_type": "elf", "e_machine": "0x28"},
        "docs/release_notes.txt": {"file_type": "text"},
        "hardware/case_print.gcode": {"file_type": "text"}
    }

    for rel_path, expected_meta in expected_files.items():
        assert rel_path in manifest, f"File {rel_path} is missing from manifest.json."

        file_meta = manifest[rel_path]
        assert "sha256" in file_meta, f"Missing 'sha256' for {rel_path} in manifest.json."
        assert file_meta.get("file_type") == expected_meta["file_type"], f"Incorrect file_type for {rel_path}."

        if expected_meta["file_type"] == "elf":
            assert "e_machine" in file_meta, f"Missing 'e_machine' for {rel_path}."
            assert file_meta["e_machine"].lower() == expected_meta["e_machine"], f"Incorrect e_machine for {rel_path}."

def test_text_files_are_utf8_encoded(extracted_archive):
    """Test that the text and gcode files in the archive are properly UTF-8 encoded."""
    text_files = [
        "artifact_staging/docs/release_notes.txt",
        "artifact_staging/hardware/case_print.gcode"
    ]

    for rel_path in text_files:
        full_path = os.path.join(extracted_archive, rel_path)
        assert os.path.isfile(full_path), f"File {rel_path} is missing from the archive."

        with open(full_path, "rb") as f:
            data = f.read()

        try:
            decoded_text = data.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail(f"File {rel_path} is not correctly encoded in UTF-8.")

        if "case_print.gcode" in rel_path:
            assert "210°C" in decoded_text, f"Expected character '°' not found or mangled in {rel_path}."

def test_hashes_match_manifest(extracted_archive):
    """Test that the SHA-256 hashes in the manifest match the actual files in the archive."""
    manifest_path = os.path.join(extracted_archive, "manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    for rel_path, meta in manifest.items():
        full_path = os.path.join(extracted_archive, "artifact_staging", rel_path)
        assert os.path.isfile(full_path), f"File {rel_path} referenced in manifest is missing from archive."

        with open(full_path, "rb") as f:
            file_data = f.read()

        actual_hash = hashlib.sha256(file_data).hexdigest()
        expected_hash = meta.get("sha256")

        assert actual_hash == expected_hash, f"SHA-256 hash mismatch for {rel_path}. Expected {expected_hash}, got {actual_hash}."
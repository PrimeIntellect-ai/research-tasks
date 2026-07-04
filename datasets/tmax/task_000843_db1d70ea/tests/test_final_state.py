# test_final_state.py

import os
import glob
import zlib
import hashlib
import pytest

PROCESSED_DOCS_DIR = "/home/user/processed_docs"

EXPECTED_DOCS = {
    "intro_001.md": (
        "---\n"
        "title: Introduction\n"
        "author: Alice\n"
        "date: 2023-01-01\n"
        "---\n\n"
        "Welcome to the documentation.\n"
    ),
    "api_002.md": (
        "---\n"
        "title: API Reference\n"
        "author: Bob\n"
        "date: 2023-01-02\n"
        "---\n\n"
        "Here is the API.\n"
    ),
    "storage_003.md": (
        "---\n"
        "title: Storage Guide\n"
        "author: Charlie\n"
        "date: 2023-01-03\n"
        "---\n\n"
        "Data storage concepts.\n"
    )
}

def test_scripts_exist():
    assert os.path.isfile("/home/user/transformer.py"), "transformer.py is missing."
    assert os.path.isfile("/home/user/compress.py"), "compress.py is missing."

def test_no_uncompressed_md_files():
    md_files = glob.glob(os.path.join(PROCESSED_DOCS_DIR, "*.md"))
    assert len(md_files) == 0, f"Uncompressed .md files should have been deleted, found: {md_files}"

def test_manifest_exists_and_correct():
    manifest_path = os.path.join(PROCESSED_DOCS_DIR, "manifest.txt")
    assert os.path.isfile(manifest_path), "manifest.txt is missing."

    with open(manifest_path, "r") as f:
        manifest_content = f.read()

    for filename, content in EXPECTED_DOCS.items():
        expected_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        assert expected_hash in manifest_content, f"Expected hash {expected_hash} for {filename} not found in manifest.txt"
        assert filename in manifest_content, f"Filename {filename} not found in manifest.txt"

def test_zlib_files_exist_and_correct():
    for filename, expected_content in EXPECTED_DOCS.items():
        zlib_filename = f"{filename}.zlib"
        zlib_path = os.path.join(PROCESSED_DOCS_DIR, zlib_filename)
        assert os.path.isfile(zlib_path), f"Compressed file {zlib_filename} is missing."

        with open(zlib_path, "rb") as f:
            compressed_data = f.read()

        try:
            decompressed_data = zlib.decompress(compressed_data).decode('utf-8')
        except Exception as e:
            pytest.fail(f"Failed to decompress {zlib_filename}: {e}")

        assert decompressed_data == expected_content, f"Decompressed content of {zlib_filename} does not match expected output."

def test_no_unexpected_files_in_processed_docs():
    expected_files = {f"{k}.zlib" for k in EXPECTED_DOCS.keys()}
    expected_files.add("manifest.txt")

    found_files = set(os.listdir(PROCESSED_DOCS_DIR))
    unexpected = found_files - expected_files
    assert not unexpected, f"Unexpected files found in processed_docs: {unexpected}"
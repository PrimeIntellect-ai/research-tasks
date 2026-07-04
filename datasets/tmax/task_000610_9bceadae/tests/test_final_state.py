# test_final_state.py

import os
import zlib
import hashlib
import csv
import pytest

ARCHIVE_DIR = "/home/user/archive"
INCOMING_DIR = "/home/user/incoming_docs"
DOCS_ARCHIVE = os.path.join(ARCHIVE_DIR, "docs.archive")
MANIFEST_CSV = os.path.join(ARCHIVE_DIR, "manifest.csv")

def test_archive_files_exist():
    assert os.path.isfile(DOCS_ARCHIVE), f"{DOCS_ARCHIVE} does not exist."
    assert os.path.isfile(MANIFEST_CSV), f"{MANIFEST_CSV} does not exist."

def test_incoming_directory_empty():
    assert os.path.isdir(INCOMING_DIR), f"{INCOMING_DIR} does not exist."
    files = os.listdir(INCOMING_DIR)
    md_files = [f for f in files if f.endswith('.md')]
    assert len(md_files) == 0, f"Found unprocessed .md files in {INCOMING_DIR}: {md_files}"

def test_manifest_and_archive_contents():
    with open(MANIFEST_CSV, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 50, f"Expected 50 rows in manifest.csv, found {len(rows)}"

    # Sort rows by offset to ensure sequential reading and logical validation
    try:
        parsed_rows = []
        for row in rows:
            filename, sha256_hex, offset, size = row
            parsed_rows.append({
                'filename': filename,
                'sha256_hex': sha256_hex,
                'offset': int(offset),
                'size': int(size)
            })
    except ValueError as e:
        pytest.fail(f"Manifest row format is incorrect: {e}")

    parsed_rows.sort(key=lambda x: x['offset'])

    with open(DOCS_ARCHIVE, 'rb') as f:
        archive_data = f.read()

    expected_offset = 0
    for i, row in enumerate(parsed_rows):
        file_num = row['filename'].replace('doc_', '').replace('.md', '')
        assert row['offset'] == expected_offset, f"Expected offset {expected_offset} for {row['filename']}, got {row['offset']}"

        compressed_chunk = archive_data[row['offset']:row['offset'] + row['size']]
        assert len(compressed_chunk) == row['size'], f"Could not read {row['size']} bytes for {row['filename']} at offset {row['offset']}"

        try:
            decompressed_bytes = zlib.decompress(compressed_chunk)
        except zlib.error as e:
            pytest.fail(f"Failed to decompress data for {row['filename']}: {e}")

        decompressed_text = decompressed_bytes.decode('utf-8')

        # Verify redaction
        assert "INTERNAL_CONFIDENTIAL" not in decompressed_text, f"Found INTERNAL_CONFIDENTIAL in {row['filename']}"
        assert "[REDACTED]" in decompressed_text, f"Did not find [REDACTED] in {row['filename']}"

        # Verify content template
        expected_text = f"# API Documentation {file_num}\nStatus: [REDACTED]\nDetails: This is the payload for endpoint {file_num}.\n"
        assert decompressed_text == expected_text, f"Content mismatch for {row['filename']}"

        # Verify SHA-256
        actual_sha256 = hashlib.sha256(decompressed_bytes).hexdigest()
        assert actual_sha256 == row['sha256_hex'], f"SHA-256 mismatch for {row['filename']}. Expected {row['sha256_hex']}, got {actual_sha256}"

        expected_offset += row['size']

    assert len(archive_data) == expected_offset, f"Archive size ({len(archive_data)}) does not match total size from manifest ({expected_offset})"
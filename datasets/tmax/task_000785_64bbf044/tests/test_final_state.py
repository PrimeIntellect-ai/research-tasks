# test_final_state.py

import os
import hashlib
import pytest

def compute_rle(text: bytes) -> bytes:
    if not text:
        return b""

    result = bytearray()
    i = 0
    n = len(text)

    while i < n:
        char = text[i]
        count = 1
        while i + count < n and text[i + count] == char and count < 255:
            count += 1

        if count >= 4:
            result.append(0x1B)
            result.append(char)
            result.append(count)
            i += count
        else:
            result.append(char)
            i += 1

    return bytes(result)

def test_processed_directory_exists():
    assert os.path.isdir("/home/user/docs_processed"), "/home/user/docs_processed directory is missing"

def test_rle_files_content():
    expected_texts = {
        "file1.rle": b"abbbbccc",
        "file2.rle": b"Helloooooo Universe",
        "file3.rle": b"A" * 256
    }

    for filename, raw_text in expected_texts.items():
        filepath = os.path.join("/home/user/docs_processed", filename)
        assert os.path.isfile(filepath), f"Expected processed file {filepath} is missing"

        expected_rle = compute_rle(raw_text)
        with open(filepath, "rb") as f:
            actual_rle = f.read()

        assert actual_rle == expected_rle, f"Content mismatch in {filename}. Expected hex: {expected_rle.hex()}, got: {actual_rle.hex()}"

def test_manifest_file():
    manifest_path = "/home/user/docs_processed/manifest.txt"
    assert os.path.isfile(manifest_path), "manifest.txt is missing"

    expected_texts = {
        "file1.rle": b"abbbbccc",
        "file2.rle": b"Helloooooo Universe",
        "file3.rle": b"A" * 256
    }

    expected_hashes = {}
    for filename, raw_text in expected_texts.items():
        expected_rle = compute_rle(raw_text)
        expected_hashes[filename] = hashlib.sha256(expected_rle).hexdigest()

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in manifest.txt, got {len(lines)}"

    # Check alphabetical order
    filenames_in_manifest = [line.split()[1] for line in lines if len(line.split()) >= 2]
    assert filenames_in_manifest == sorted(filenames_in_manifest), "Manifest entries are not sorted alphabetically by filename"

    for line in lines:
        parts = line.split()
        assert len(parts) == 2, f"Invalid manifest line format: {line}"
        file_hash, filename = parts

        # Strip leading paths if any (requirement says paths in manifest are just filenames)
        assert "/" not in filename, f"Manifest should only contain base filenames, found: {filename}"
        assert filename in expected_hashes, f"Unexpected filename in manifest: {filename}"
        assert file_hash == expected_hashes[filename], f"Hash mismatch for {filename} in manifest"
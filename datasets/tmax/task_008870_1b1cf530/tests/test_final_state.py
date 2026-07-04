# test_final_state.py

import os
import tarfile
import hashlib
import pytest

DRAFTS_DIR = "/home/user/drafts"
TAR_FILE = "/home/user/release.tar.gz"
CPP_BIN = "/home/user/process_docs"

EXPECTED_TXT_FILES = {
    "doc_01.txt": b"Apple docs\n",
    "doc_02.txt": b"Banana docs\n",
    "doc_03.txt": b"Cherry docs\n",
    "doc_04.txt": b"Mango docs\n",
    "doc_05.txt": b"Zebra docs\n",
}

EXPECTED_CHUNKS = {
    "diagram.dat.chunk001": 100000,
    "diagram.dat.chunk002": 100000,
    "diagram.dat.chunk003": 50000,
    "screenshot.dat.chunk001": 100000,
    "screenshot.dat.chunk002": 50000,
}

OLD_FILES = [
    "apple.txt", "zebra.txt", "mango.txt", "banana.txt", "cherry.txt",
    "diagram.dat", "screenshot.dat"
]

def get_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_cpp_program_exists():
    assert os.path.isfile(CPP_BIN), f"C++ program {CPP_BIN} does not exist."
    assert os.access(CPP_BIN, os.X_OK), f"C++ program {CPP_BIN} is not executable."

def test_old_files_deleted():
    for old_file in OLD_FILES:
        filepath = os.path.join(DRAFTS_DIR, old_file)
        assert not os.path.exists(filepath), f"Original file {old_file} was not deleted."

def test_renamed_txt_files():
    for filename, expected_content in EXPECTED_TXT_FILES.items():
        filepath = os.path.join(DRAFTS_DIR, filename)
        assert os.path.isfile(filepath), f"Renamed file {filename} does not exist."
        with open(filepath, "rb") as f:
            content = f.read()
        assert content == expected_content, f"Content of {filename} is incorrect. Expected {expected_content}, got {content}."

def test_chunked_dat_files():
    for filename, expected_size in EXPECTED_CHUNKS.items():
        filepath = os.path.join(DRAFTS_DIR, filename)
        assert os.path.isfile(filepath), f"Chunk file {filename} does not exist."
        actual_size = os.path.getsize(filepath)
        assert actual_size == expected_size, f"Size of {filename} is {actual_size}, expected {expected_size}."

def test_manifest_file():
    manifest_path = os.path.join(DRAFTS_DIR, "manifest.tsv")
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    expected_files = list(EXPECTED_TXT_FILES.keys()) + list(EXPECTED_CHUNKS.keys())
    expected_files.sort()

    with open(manifest_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_files), f"Manifest should have {len(expected_files)} lines, but has {len(lines)}."

    for i, line in enumerate(lines):
        parts = line.split('\t')
        assert len(parts) == 3, f"Manifest line {i+1} is not correctly tab-separated: {line}"
        filename, size, sha256 = parts

        assert filename == expected_files[i], f"Manifest line {i+1} filename mismatch. Expected {expected_files[i]}, got {filename}."

        filepath = os.path.join(DRAFTS_DIR, filename)
        assert os.path.isfile(filepath), f"File {filename} listed in manifest does not exist."

        actual_size = str(os.path.getsize(filepath))
        assert size == actual_size, f"Manifest line {i+1} size mismatch for {filename}. Expected {actual_size}, got {size}."

        actual_sha256 = get_sha256(filepath)
        assert sha256 == actual_sha256, f"Manifest line {i+1} SHA256 mismatch for {filename}. Expected {actual_sha256}, got {sha256}."

def test_release_tar_gz():
    assert os.path.isfile(TAR_FILE), f"Archive {TAR_FILE} does not exist."

    with tarfile.open(TAR_FILE, "r:gz") as tar:
        members = tar.getnames()

    expected_files = list(EXPECTED_TXT_FILES.keys()) + list(EXPECTED_CHUNKS.keys()) + ["manifest.tsv"]

    assert len(members) == len(expected_files), f"Archive should contain exactly {len(expected_files)} files, but contains {len(members)}."

    for member in members:
        assert "/" not in member, f"Archive should not contain outer folder structure, but found {member}."
        assert member in expected_files, f"Archive contains unexpected file {member}."
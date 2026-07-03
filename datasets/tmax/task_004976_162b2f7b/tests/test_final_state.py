# test_final_state.py
import os
import json
import gzip
import hashlib
import tarfile
import pytest

INCOMING_DIR = "/home/user/incoming"
CURATED_DIR = "/home/user/curated"
MANIFEST_PATH = "/home/user/curated/manifest.json"
ARCHIVE_PATH = "/home/user/curated_archive.tar.gz"

def get_expected_state():
    """Computes the expected state from the incoming directory."""
    expected_manifest = {}
    valid_elfs = []

    if not os.path.isdir(INCOMING_DIR):
        return expected_manifest, valid_elfs

    for fname in sorted(os.listdir(INCOMING_DIR)):
        if not fname.endswith(".gz"):
            continue
        path = os.path.join(INCOMING_DIR, fname)
        with gzip.open(path, 'rb') as f:
            data = f.read()

        if data.startswith(b'\x7fELF'):
            out_name = fname[:-3]
            sha256 = hashlib.sha256(data).hexdigest()
            expected_manifest[out_name] = sha256
            valid_elfs.append((out_name, sha256))

    return expected_manifest, valid_elfs

def test_curated_directory_exists():
    assert os.path.isdir(CURATED_DIR), f"Directory {CURATED_DIR} does not exist"

def test_manifest_content():
    expected_manifest, _ = get_expected_state()
    assert os.path.isfile(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} is missing"

    with open(MANIFEST_PATH, 'r') as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Manifest is not valid JSON")

    assert manifest == expected_manifest, "Manifest contents do not match the expected valid ELFs and checksums"

def test_curated_files_exist_and_no_garbage():
    expected_manifest, _ = get_expected_state()
    curated_files = set(os.listdir(CURATED_DIR))
    curated_files.discard("manifest.json")

    expected_files = set(expected_manifest.keys())

    missing = expected_files - curated_files
    assert not missing, f"Missing valid ELF files in curated directory: {missing}"

    extra = curated_files - expected_files
    assert not extra, f"Found unexpected files (or garbage) in curated directory: {extra}"

def test_hard_links_for_duplicates():
    _, valid_elfs = get_expected_state()

    # Group by checksum
    checksum_to_files = {}
    for fname, sha256 in valid_elfs:
        checksum_to_files.setdefault(sha256, []).append(fname)

    for sha256, fnames in checksum_to_files.items():
        if not fnames:
            continue

        first_file = os.path.join(CURATED_DIR, fnames[0])
        assert os.path.isfile(first_file), f"File {first_file} is missing"
        first_inode = os.stat(first_file).st_ino

        # Check that all duplicates share the same inode
        for duplicate in fnames[1:]:
            dup_file = os.path.join(CURATED_DIR, duplicate)
            assert os.path.isfile(dup_file), f"File {dup_file} is missing"
            dup_inode = os.stat(dup_file).st_ino
            assert dup_inode == first_inode, f"File {duplicate} is not a hard link to {fnames[0]}"

def test_archive_exists_and_valid():
    assert os.path.isfile(ARCHIVE_PATH), f"Archive {ARCHIVE_PATH} is missing"
    assert tarfile.is_tarfile(ARCHIVE_PATH), f"{ARCHIVE_PATH} is not a valid tar archive"

    expected_manifest, _ = get_expected_state()
    expected_basenames = set(expected_manifest.keys()) | {"manifest.json"}

    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        members = tar.getmembers()
        # Extract basenames of files in the tarball
        archive_basenames = {os.path.basename(m.name) for m in members if m.isfile()}

        missing = expected_basenames - archive_basenames
        assert not missing, f"Archive is missing expected files: {missing}"
# test_final_state.py

import os
import hashlib
import pytest

EXTRACT_DIR = '/home/user/extracted_configs'
MANIFEST_FILE = '/home/user/manifest.txt'
BASHRC_FILE = '/home/user/.bashrc'

EXPECTED_FILES = {
    'database.conf': b'host=localhost\nport=5432\n',
    'logging.conf': b'level=DEBUG\n',
    'cache.conf': b'redis_port=6379\n'
}

def get_sha256(filepath):
    """Helper to compute SHA256 of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_extracted_directory_exists():
    assert os.path.isdir(EXTRACT_DIR), f"The directory {EXTRACT_DIR} was not created."

def test_correct_files_extracted():
    extracted_files = set(os.listdir(EXTRACT_DIR))
    expected_filenames = set(EXPECTED_FILES.keys())

    missing = expected_filenames - extracted_files
    extra = extracted_files - expected_filenames

    assert not missing, f"Missing expected files in {EXTRACT_DIR}: {missing}"
    assert not extra, f"Found unexpected files in {EXTRACT_DIR}: {extra}"

def test_extracted_file_contents():
    for filename, expected_content in EXPECTED_FILES.items():
        filepath = os.path.join(EXTRACT_DIR, filename)
        with open(filepath, 'rb') as f:
            content = f.read()
        assert content == expected_content, f"Content of {filename} does not match expected original content."

def test_malicious_archive_skipped():
    # The entire malicious archive should be skipped, so benign.conf shouldn't be extracted
    benign_path = os.path.join(EXTRACT_DIR, 'benign.conf')
    assert not os.path.exists(benign_path), "Malicious archive was processed! 'benign.conf' was extracted."

    # Check if zip slip payload was written
    if os.path.exists(BASHRC_FILE):
        with open(BASHRC_FILE, 'r') as f:
            content = f.read()
        assert 'echo "hacked"' not in content, "Zip Slip vulnerability was successfully exploited! .bashrc was overwritten."

def test_ignored_archive_skipped():
    # ignored_update.zip is not in config.json and should not be processed
    ignored_path = os.path.join(EXTRACT_DIR, 'ignored.conf')
    assert not os.path.exists(ignored_path), "Files from an archive not listed in config.json were extracted."

def test_manifest_exists_and_correct():
    assert os.path.isfile(MANIFEST_FILE), f"The manifest file {MANIFEST_FILE} was not created."

    # Dynamically compute expected manifest based on actual extracted files (which we verified above)
    expected_lines = []
    for filename in sorted(EXPECTED_FILES.keys()):
        filepath = os.path.join(EXTRACT_DIR, filename)
        file_hash = get_sha256(filepath)
        expected_lines.append(f"{file_hash}  {filename}")

    expected_manifest_content = "\n".join(expected_lines) + "\n"

    with open(MANIFEST_FILE, 'r') as f:
        actual_manifest_content = f.read()

    # Strip trailing newlines for a cleaner comparison if the student missed the final newline,
    # but strictly check the format of the lines.
    actual_lines = [line for line in actual_manifest_content.splitlines() if line.strip()]
    expected_lines_clean = [line for line in expected_manifest_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines_clean, (
        f"Manifest contents are incorrect or incorrectly formatted.\n"
        f"Expected:\n{chr(10).join(expected_lines_clean)}\n\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )
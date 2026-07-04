# test_final_state.py
import os
import pytest

EXPECTED_FILES = {
    "file_a.log": "Log entry 1: RESOLVED_01 found.",
    "file_b.log": "No errors here. Just standard text.",
    "file_c.log": "Critical RESOLVED_01 and another RESOLVED_01!"
}

PROCESSED_DIR = "/home/user/processed"
LINKS_DIR = "/home/user/links"

def test_processed_files_exist_and_content():
    """Check that processed files exist, are valid UTF-8, and have correct content."""
    for filename, expected_text in EXPECTED_FILES.items():
        filepath = os.path.join(PROCESSED_DIR, filename)
        assert os.path.isfile(filepath), f"Processed file missing: {filepath}"

        # Read as bytes to check for null bytes (UTF-16 leftover check)
        with open(filepath, "rb") as f:
            content_bytes = f.read()

        assert b'\x00' not in content_bytes, f"File {filepath} contains null bytes, likely not properly converted to UTF-8."

        # Decode as UTF-8
        try:
            content_str = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail(f"File {filepath} is not valid UTF-8.")

        assert content_str == expected_text, f"Content mismatch in {filepath}. Expected '{expected_text}', got '{content_str}'"

def test_hard_links_exist_and_correct():
    """Check that hard links exist and share the same inode as the processed files."""
    for filename in EXPECTED_FILES.keys():
        processed_path = os.path.join(PROCESSED_DIR, filename)
        link_path = os.path.join(LINKS_DIR, filename)

        assert os.path.isfile(link_path), f"Link file missing: {link_path}"

        stat_proc = os.stat(processed_path)
        stat_link = os.stat(link_path)

        assert stat_proc.st_ino == stat_link.st_ino, f"{link_path} is not a hard link to {processed_path}"
        assert stat_proc.st_dev == stat_link.st_dev, f"{link_path} and {processed_path} are on different devices"
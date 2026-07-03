# test_final_state.py

import os
import pytest

def test_extracted_files_exist_and_contents_match():
    target_dir = "/home/user/extracted_docs"

    expected_files = {
        "doc_intro.html": b"<html><body><p>Welcome to the system.</p></body></html>",
        "doc_id_rsa.txt": b"fake_key_data_123",
        "doc_important_notice.html": b"<html><body><p>System maintenance on Friday.</p></body></html>",
        "doc_config.json": b'{"status": "ok"}'
    }

    # Check that directory exists
    assert os.path.exists(target_dir), f"Directory {target_dir} is missing."
    assert os.path.isdir(target_dir), f"{target_dir} is not a directory."

    # Check that exactly these 4 files exist
    actual_files = os.listdir(target_dir)
    assert len(actual_files) == 4, f"Expected exactly 4 files in {target_dir}, but found {len(actual_files)}: {actual_files}"

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(target_dir, filename)
        assert os.path.exists(filepath), f"Expected file {filepath} is missing."
        assert os.path.isfile(filepath), f"{filepath} is not a file."

        with open(filepath, "rb") as f:
            actual_content = f.read()

        assert actual_content == expected_content, f"Content mismatch in {filepath}. Expected {expected_content}, got {actual_content}"
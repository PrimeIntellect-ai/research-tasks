# test_final_state.py

import os
import tarfile
import json
import tempfile
import pytest

BACKUP_FILE = "/home/user/backup.tar.xz"
DOCS_DIR = "/app/docs"

def test_backup_efficiency_and_completeness():
    assert os.path.exists(BACKUP_FILE), f"Backup file {BACKUP_FILE} not found."
    archive_size = os.path.getsize(BACKUP_FILE)
    assert archive_size > 0, "Backup file is empty."

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with tarfile.open(BACKUP_FILE, "r:xz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.ReadError:
            pytest.fail(f"Backup file {BACKUP_FILE} is not a valid tar.xz archive.")

        # Find all extracted files
        extracted_files = {}
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                # Store the absolute path of the extracted file, keyed by its basename
                extracted_files[file] = os.path.join(root, file)

        # Check original files
        if os.path.exists(DOCS_DIR):
            original_files = os.listdir(DOCS_DIR)
        else:
            original_files = []

        original_txt_md = [f for f in original_files if f.endswith(('.txt', '.md'))]
        original_media = [f for f in original_files if f.endswith('.media')]

        raw_text_size = 0
        for f in original_txt_md:
            assert f in extracted_files, f"Missing file in archive: {f}"
            extracted_path = extracted_files[f]

            # Verify valid UTF-8
            with open(extracted_path, "rb") as ext_file:
                content = ext_file.read()
                try:
                    content.decode('utf-8')
                except UnicodeDecodeError:
                    pytest.fail(f"File {f} is not valid UTF-8 in the archive.")

            raw_text_size += os.path.getsize(extracted_path)

        # Verify media_headers.json
        assert "media_headers.json" in extracted_files, "media_headers.json is missing in the archive."
        headers_file = extracted_files["media_headers.json"]
        header_data_size = os.path.getsize(headers_file)

        with open(headers_file, "r") as hf:
            try:
                media_headers = json.load(hf)
            except json.JSONDecodeError:
                pytest.fail("media_headers.json is not valid JSON.")

        for f in original_media:
            assert f in media_headers, f"Missing header for {f} in media_headers.json"

            # Read actual first 32 bytes from the original media file
            with open(os.path.join(DOCS_DIR, f), "rb") as media_file:
                actual_header = media_file.read(32).hex()

            assert media_headers[f] == actual_header, f"Incorrect header extracted for {f}. Expected {actual_header}, got {media_headers[f]}"

        efficiency_score = (raw_text_size + header_data_size) / archive_size
        assert efficiency_score >= 4.5, f"Efficiency score {efficiency_score:.2f} is below threshold 4.5. Archive size: {archive_size}, Text size: {raw_text_size}, Header size: {header_data_size}"
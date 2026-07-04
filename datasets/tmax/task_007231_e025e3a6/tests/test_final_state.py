# test_final_state.py

import os
import tarfile
import tempfile
import pytest

def test_zip_slip_mitigated():
    """Ensure the malicious path did not overwrite files outside the safe zone."""
    assert not os.path.exists('/home/user/data.csv'), (
        "Zip slip vulnerability was not mitigated; /home/user/data.csv was created."
    )

def test_clean_logs_archive_exists():
    """Check that the final compressed archive exists."""
    archive_path = '/home/user/clean_logs.tar.bz2'
    assert os.path.isfile(archive_path), f"{archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tarball."

def test_archive_contents_and_redaction():
    """Extract the archive and verify the flattened structure, conversions, splits, and redactions."""
    archive_path = '/home/user/clean_logs.tar.bz2'
    if not os.path.isfile(archive_path) or not tarfile.is_tarfile(archive_path):
        pytest.fail("Cannot test contents because archive is missing or invalid.")

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, 'r:bz2') as tar:
            tar.extractall(path=tmpdir)

        # The archive might contain files directly or inside a 'safe_zone' dir.
        # Let's find the actual files.
        extracted_files = []
        for root, _, files in os.walk(tmpdir):
            for f in files:
                extracted_files.append(os.path.relpath(os.path.join(root, f), tmpdir))

        # Extract base filenames to check flattening
        base_files = [os.path.basename(f) for f in extracted_files]

        # 1. Flattening check: access.log should exist
        assert 'access.log' in base_files, "access.log not found in archive. Flattening may have failed."

        # 2. CSV to TSV conversion
        assert 'data.tsv' in base_files, "data.tsv not found; CSV to TSV conversion failed."
        assert 'data.csv' not in base_files, "data.csv still exists in archive; it should have been removed."

        # 3. Chunking check
        assert 'server.log.partaa' in base_files, "server.log.partaa not found; splitting failed."
        assert 'server.log.partab' in base_files, "server.log.partab not found; splitting failed."
        assert 'server.log' not in base_files, "server.log still exists; it should have been removed after splitting."

        # Helper to read file content
        def read_file_content(basename):
            for f in extracted_files:
                if os.path.basename(f) == basename:
                    with open(os.path.join(tmpdir, f), 'r') as file_obj:
                        return file_obj.read()
            return ""

        # 4. Redaction and TSV format checks
        data_tsv_content = read_file_content('data.tsv')
        assert "1\talice\t***" in data_tsv_content, (
            "data.tsv does not contain the expected tab-separated and redacted content."
        )
        assert "," not in data_tsv_content, "data.tsv still contains commas."

        access_log_content = read_file_content('access.log')
        assert "User login from ***" in access_log_content, "access.log was not properly redacted."
        assert "192.168.1.100" not in access_log_content, "Unredacted IP found in access.log."

        server_partaa_content = read_file_content('server.log.partaa')
        assert "Line 1: ***" in server_partaa_content, "server.log.partaa was not properly redacted."
        assert "192.168.1.1" not in server_partaa_content, "Unredacted IP found in server.log.partaa."
        assert len(server_partaa_content.strip().split('\n')) == 5, "server.log.partaa does not have exactly 5 lines."
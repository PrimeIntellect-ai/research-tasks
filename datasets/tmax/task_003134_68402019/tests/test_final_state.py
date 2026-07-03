# test_final_state.py

import os
import tarfile
import tempfile
import hashlib
import pytest

BACKUP_ARCHIVE = "/home/user/backup.tar.gz"

APP1_EXPECTED = """INFO 2023-10-01 Starting service
DEBUG USER=alice PASSWORD=[REDACTED] IP=192.168.1.5
INFO User logged in
ERROR USER=bob PASSWORD=[REDACTED] Connection failed
"""

APP2_EXPECTED = """INFO 2023-10-02 Service running normally
DEBUG USER=admin PASSWORD=[REDACTED]
INFO USER=charlie PASSWORD=[REDACTED] IP=10.0.0.2
"""

def test_backup_archive_exists():
    assert os.path.isfile(BACKUP_ARCHIVE), f"Backup archive {BACKUP_ARCHIVE} does not exist."

def test_backup_contents_and_redaction():
    assert os.path.isfile(BACKUP_ARCHIVE), f"Backup archive {BACKUP_ARCHIVE} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with tarfile.open(BACKUP_ARCHIVE, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError as e:
            pytest.fail(f"Failed to extract {BACKUP_ARCHIVE}: {e}")

        clean_logs_dir = os.path.join(tmpdir, "clean_logs")
        assert os.path.isdir(clean_logs_dir), "'clean_logs' directory not found in the archive."

        app1_path = os.path.join(clean_logs_dir, "app1.log")
        app2_path = os.path.join(clean_logs_dir, "app2.log")
        manifest_path = os.path.join(clean_logs_dir, "manifest.sha256")

        assert os.path.isfile(app1_path), "app1.log not found in clean_logs directory."
        assert os.path.isfile(app2_path), "app2.log not found in clean_logs directory."
        assert os.path.isfile(manifest_path), "manifest.sha256 not found in clean_logs directory."

        with open(app1_path, "r") as f:
            app1_content = f.read()
        assert app1_content == APP1_EXPECTED, "app1.log content was not properly redacted."

        with open(app2_path, "r") as f:
            app2_content = f.read()
        assert app2_content == APP2_EXPECTED, "app2.log content was not properly redacted."

        # Calculate SHA256 of extracted files
        app1_sha256 = hashlib.sha256(app1_content.encode('utf-8')).hexdigest()
        app2_sha256 = hashlib.sha256(app2_content.encode('utf-8')).hexdigest()

        with open(manifest_path, "r") as f:
            manifest_lines = f.read().strip().splitlines()

        manifest_dict = {}
        for line in manifest_lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                # the filename might have a leading '*' or ' ' depending on sha256sum mode
                filename = parts[1].lstrip('*')
                manifest_dict[filename] = parts[0]

        assert "app1.log" in manifest_dict, "app1.log missing from manifest.sha256"
        assert "app2.log" in manifest_dict, "app2.log missing from manifest.sha256"

        assert manifest_dict["app1.log"] == app1_sha256, "app1.log checksum in manifest does not match actual checksum."
        assert manifest_dict["app2.log"] == app2_sha256, "app2.log checksum in manifest does not match actual checksum."
# test_final_state.py

import os
import re
import tarfile
import hashlib

def test_backup_archive_exists_and_contents():
    archive_path = "/home/user/backups/mailer_backup.tar.gz"
    assert os.path.isfile(archive_path), f"Backup archive {archive_path} does not exist."

    # Check contents
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            names = tar.getnames()
    except tarfile.TarError as e:
        assert False, f"Failed to open tar archive {archive_path}: {e}"

    # Verify paths ending in config.cf and templates/welcome.txt exist in the tar
    has_config = any(name.endswith("config.cf") for name in names)
    has_welcome = any(name.endswith("templates/welcome.txt") for name in names)

    assert has_config, "config.cf is missing from the backup archive."
    assert has_welcome, "templates/welcome.txt is missing from the backup archive."

def test_deployment_summary_log_and_checksum():
    log_path = "/home/user/deployment_summary.log"
    archive_path = "/home/user/backups/mailer_backup.tar.gz"

    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    assert os.path.isfile(archive_path), f"Archive {archive_path} missing for checksum calculation."

    with open(log_path, "r") as f:
        log_content = f.read()

    match = re.search(r"BACKUP_CHECKSUM:\s*([a-f0-9]{32})", log_content)
    assert match is not None, f"Could not find BACKUP_CHECKSUM with a valid MD5 hash in {log_path}."

    logged_hash = match.group(1)

    # Compute actual MD5 hash
    md5 = hashlib.md5()
    with open(archive_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)

    actual_hash = md5.hexdigest()

    assert logged_hash == actual_hash, f"Logged MD5 hash ({logged_hash}) does not match actual hash ({actual_hash})."

def test_script_hardening():
    script_path = "/home/user/scripts/backup_mailer.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "set -euo pipefail" in content, f"'set -euo pipefail' is missing from {script_path}."
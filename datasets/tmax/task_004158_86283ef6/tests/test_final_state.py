# test_final_state.py

import os
import subprocess
import gzip
import tarfile
import shutil
import pytest

BACKUP_SCRIPT = "/home/user/scripts/backup.sh"
ROTATE_SCRIPT = "/home/user/scripts/rotate_logs.sh"
SANITIZER_BIN = "/home/user/backend/sanitizer"
BACKUP_ARCHIVE = "/home/user/archives/secure_backups/data_backup.tar.gz"
BACKEND_DATA_DIR = "/home/user/backend/data"
LOG_FILE = "/home/user/backend/logs/server.log"
ROTATED_LOG_FILE = "/home/user/backend/logs/server.log.1.gz"
EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"

def test_backup_script():
    assert os.path.isfile(BACKUP_SCRIPT), f"Backup script {BACKUP_SCRIPT} not found."

    # Run backup script in restricted environment
    result = subprocess.run(
        ["bash", BACKUP_SCRIPT],
        env={"PATH": ""},
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Backup script failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    assert os.path.isfile(BACKUP_ARCHIVE), f"Backup archive {BACKUP_ARCHIVE} was not created."

    # Verify tar contents
    try:
        with tarfile.open(BACKUP_ARCHIVE, "r:gz") as tar:
            tar_names = tar.getnames()
    except Exception as e:
        pytest.fail(f"Failed to open {BACKUP_ARCHIVE} as a tar.gz file: {e}")

    # Check if the data directory contents are in the tar
    data_files = []
    for root, _, files in os.walk(BACKEND_DATA_DIR):
        for file in files:
            data_files.append(os.path.relpath(os.path.join(root, file), BACKEND_DATA_DIR))

    # Simple check: the archive should contain at least the files in data_files
    # Tar names might include the top-level directory or just the files
    tar_basenames = [os.path.basename(name) for name in tar_names]
    for df in data_files:
        df_basename = os.path.basename(df)
        assert df_basename in tar_basenames, f"File {df_basename} from data directory not found in the backup archive."

def test_log_rotation():
    assert os.path.isfile(ROTATE_SCRIPT), f"Rotate script {ROTATE_SCRIPT} not found."

    # Create 2MB dummy log file
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "wb") as f:
        f.write(os.urandom(2 * 1024 * 1024))

    result = subprocess.run(
        ["bash", ROTATE_SCRIPT],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Rotate script failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    assert os.path.isfile(LOG_FILE), f"Original log file {LOG_FILE} missing after rotation."
    assert os.path.getsize(LOG_FILE) == 0, f"Original log file {LOG_FILE} was not truncated to 0 bytes."

    assert os.path.isfile(ROTATED_LOG_FILE), f"Rotated log file {ROTATED_LOG_FILE} missing."
    try:
        with gzip.open(ROTATED_LOG_FILE, "rb") as f:
            f.read(1024)
    except Exception as e:
        pytest.fail(f"Rotated log file {ROTATED_LOG_FILE} is not a valid gzip file: {e}")

def test_sanitizer():
    assert os.path.isfile(SANITIZER_BIN), f"Sanitizer binary {SANITIZER_BIN} not found."
    assert os.access(SANITIZER_BIN, os.X_OK), f"Sanitizer binary {SANITIZER_BIN} is not executable."

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    for evil in evil_files:
        result = subprocess.run([SANITIZER_BIN, evil], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(evil))

    for clean in clean_files:
        result = subprocess.run([SANITIZER_BIN, clean], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(clean))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))
# test_final_state.py

import os
import re
import pytest

BACKUP_OPS_DIR = "/home/user/backup_ops"
UTF8_LOG = os.path.join(BACKUP_OPS_DIR, "legacy_app_utf8.log")
UPDATER_C = os.path.join(BACKUP_OPS_DIR, "updater.c")
UPDATER_BIN = os.path.join(BACKUP_OPS_DIR, "updater")
CATALOG_TXT = os.path.join(BACKUP_OPS_DIR, "catalog.txt")

def test_utf8_log_exists_and_valid():
    assert os.path.isfile(UTF8_LOG), f"File {UTF8_LOG} does not exist."

    try:
        with open(UTF8_LOG, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"File {UTF8_LOG} is not valid UTF-8.")

    assert "FATAL" in content, f"Expected content not found in {UTF8_LOG}."

def test_updater_c_exists_and_contains_lock():
    assert os.path.isfile(UPDATER_C), f"File {UPDATER_C} does not exist."

    with open(UPDATER_C, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    assert "flock" in content or "fcntl" in content, f"File {UPDATER_C} does not contain 'flock' or 'fcntl' for file locking."

def test_updater_bin_exists_and_executable():
    assert os.path.isfile(UPDATER_BIN), f"Executable {UPDATER_BIN} does not exist."
    assert os.access(UPDATER_BIN, os.X_OK), f"File {UPDATER_BIN} is not executable."

def test_catalog_txt_updated():
    assert os.path.isfile(CATALOG_TXT), f"File {CATALOG_TXT} does not exist."

    with open(CATALOG_TXT, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    expected_line = "legacy_app_utf8.log recorded 3 FATAL events"
    assert expected_line in content, f"Expected line '{expected_line}' not found in {CATALOG_TXT}."
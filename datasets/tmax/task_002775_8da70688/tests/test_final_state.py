# test_final_state.py

import os
import sys
import subprocess
import pytest

CLEAN_DIR = "/home/user/data/clean"
EVIL_DIR = "/home/user/data/evil"
SCRIPT = "/home/user/hierarchy_validator.py"

def test_script_exists():
    assert os.path.isfile(SCRIPT), f"Script {SCRIPT} not found."

def test_clean_corpus():
    if not os.path.isdir(CLEAN_DIR):
        pytest.skip(f"Clean dir {CLEAN_DIR} missing")

    clean_files = [os.path.join(CLEAN_DIR, f) for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    failed = []

    for f in clean_files:
        result = subprocess.run(["python3", SCRIPT, f], capture_output=True, text=True)
        basename = os.path.basename(f)
        if result.returncode != 0 or f"CLEAN: {basename}" not in result.stdout:
            failed.append(basename)

    assert not failed, f"{len(failed)} of {len(clean_files)} clean modified/rejected: {', '.join(failed)}"

def test_evil_corpus():
    if not os.path.isdir(EVIL_DIR):
        pytest.skip(f"Evil dir {EVIL_DIR} missing")

    evil_files = [os.path.join(EVIL_DIR, f) for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    failed = []

    for f in evil_files:
        result = subprocess.run(["python3", SCRIPT, f], capture_output=True, text=True)
        basename = os.path.basename(f)
        if result.returncode != 1 or f"EVIL: {basename}" not in result.stdout:
            failed.append(basename)

    assert not failed, f"{len(failed)} of {len(evil_files)} evil bypassed: {', '.join(failed)}"

def test_vendored_package_fixed():
    """Test that the sqlite-utils package bug was fixed."""
    vendored_path = "/app/sqlite-utils-3.35"
    if not os.path.isdir(vendored_path):
        pytest.fail(f"Vendored path {vendored_path} is missing.")

    sys.path.insert(0, vendored_path)
    try:
        import sqlite_utils
    except ImportError:
        pytest.fail("Failed to import sqlite_utils from vendored path.")

    db = sqlite_utils.Database(memory=True)

    # Insert rows with duplicate parent_ids
    rows = [{"id": i, "parent_id": 1} for i in range(2, 100)]
    db["hierarchy"].insert_all(rows)

    try:
        # If the bug is present, this will attempt to create a UNIQUE index and raise an IntegrityError
        db["hierarchy"].create_index(["parent_id"])
    except Exception as e:
        pytest.fail(f"Vendored package bug not fixed. Creating index failed with: {e}")

    count = db.execute("SELECT count(*) FROM hierarchy").fetchone()[0]
    assert count == 98, f"Vendored package bug not fixed: expected 98 rows, got {count}."
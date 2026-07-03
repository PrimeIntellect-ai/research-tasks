# test_final_state.py
import os
import gzip
import json
import pytest

RAW_LOGS_DIR = "/home/user/raw_logs"
ORGANIZED_LOGS_DIR = "/home/user/organized_logs"
MANIFEST_FILE = os.path.join(ORGANIZED_LOGS_DIR, "manifest.log")

@pytest.fixture(scope="module")
def expected_state():
    """
    Parses the raw logs to determine the expected final state.
    Returns a dict with:
      - 'hard_links': list of dicts with src_path, dest_path, app_id, timestamp, original_filename
      - 'latest_symlinks': dict mapping app_id to the expected latest filename
      - 'manifest_lines': list of expected lines in the manifest
    """
    hard_links = []
    latest_by_app = {}
    manifest_lines = []

    for root, _, files in os.walk(RAW_LOGS_DIR):
        for file in files:
            if file.endswith(".gz"):
                src_path = os.path.join(root, file)
                try:
                    with gzip.open(src_path, 'rt', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        metadata = json.loads(first_line)
                except Exception as e:
                    pytest.fail(f"Could not read raw log {src_path}: {e}")

                app_id = metadata.get("app_id")
                timestamp = metadata.get("timestamp")

                if not app_id or not timestamp:
                    continue

                dest_filename = f"{timestamp}_{file}"
                dest_path = os.path.join(ORGANIZED_LOGS_DIR, app_id, dest_filename)

                hard_links.append({
                    "src_path": src_path,
                    "dest_path": dest_path,
                    "app_id": app_id,
                    "timestamp": timestamp,
                    "original_filename": file
                })

                manifest_lines.append(f"LINKED {file} TO {app_id}")

                if app_id not in latest_by_app or timestamp > latest_by_app[app_id]["timestamp"]:
                    latest_by_app[app_id] = {
                        "timestamp": timestamp,
                        "filename": dest_filename
                    }

    return {
        "hard_links": hard_links,
        "latest_symlinks": latest_by_app,
        "manifest_lines": manifest_lines
    }

def test_hard_links_created(expected_state):
    """Test that all expected hard links are created and inodes match."""
    for link_info in expected_state["hard_links"]:
        src_path = link_info["src_path"]
        dest_path = link_info["dest_path"]

        assert os.path.exists(dest_path), f"Expected hard link missing: {dest_path}"

        src_inode = os.stat(src_path).st_ino
        dest_inode = os.stat(dest_path).st_ino

        assert src_inode == dest_inode, \
            f"Inode mismatch for {dest_path}. Expected it to be a hard link to {src_path}."

def test_symlinks_for_latest_logs(expected_state):
    """Test that symlinks for the latest logs are created correctly per app_id."""
    for app_id, latest_info in expected_state["latest_symlinks"].items():
        symlink_path = os.path.join(ORGANIZED_LOGS_DIR, app_id, "latest.gz")

        assert os.path.islink(symlink_path), f"Expected symlink missing or not a symlink: {symlink_path}"

        target = os.readlink(symlink_path)
        expected_target_ending = latest_info["filename"]

        assert target.endswith(expected_target_ending), \
            f"Symlink {symlink_path} points to {target}, expected it to point to {expected_target_ending}"

def test_manifest_file_contents(expected_state):
    """Test that the manifest file contains exactly the expected lines, unbroken."""
    assert os.path.exists(MANIFEST_FILE), f"Manifest file missing: {MANIFEST_FILE}"

    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
        actual_lines = f.read().splitlines()

    expected_lines = expected_state["manifest_lines"]

    assert len(actual_lines) == len(expected_lines), \
        f"Manifest has {len(actual_lines)} lines, expected {len(expected_lines)}."

    # Check counts of each expected line to ensure no partial writes or missing entries
    for line in set(expected_lines):
        expected_count = expected_lines.count(line)
        actual_count = actual_lines.count(line)
        assert actual_count == expected_count, \
            f"Manifest line '{line}' appears {actual_count} times, expected {expected_count}."
# test_final_state.py
import os
import re
import zlib
import pytest

def get_latest_success_timestamp(log_path):
    assert os.path.exists(log_path), f"Log file {log_path} missing."
    with open(log_path, 'r') as f:
        content = f.read()

    records = content.split('--- Backup Record ---')
    max_ts = -1
    for record in records:
        if not record.strip():
            continue
        if 'Status: SUCCESS' in record:
            match = re.search(r'Timestamp:\s*(\d+)', record)
            if match:
                ts = int(match.group(1))
                if ts > max_ts:
                    max_ts = ts
    return max_ts

def build_expected_archive(base_dir, min_mtime):
    files_to_archive = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.islink(full_path):
                continue

            stat = os.stat(full_path)
            if stat.st_mtime > min_mtime:
                rel_path = os.path.relpath(full_path, base_dir)
                files_to_archive.append(rel_path)

    files_to_archive.sort()

    archive_parts = []
    for rel_path in files_to_archive:
        full_path = os.path.join(base_dir, rel_path)
        size = os.path.getsize(full_path)
        with open(full_path, 'rb') as f:
            content = f.read().decode('utf-8')
        archive_parts.append(f"{rel_path}\n{size}\n{content}")

    return "".join(archive_parts)

def test_latest_backup_zlib_content():
    log_path = '/home/user/backup_history.log'
    base_dir = '/home/user/data'
    target_backup = '/home/user/latest_backup.zlib'

    latest_success_ts = get_latest_success_timestamp(log_path)
    assert latest_success_ts != -1, "Could not find a successful backup timestamp in the log."

    expected_data = build_expected_archive(base_dir, latest_success_ts)

    assert os.path.exists(target_backup), f"Backup file {target_backup} was not created."

    with open(target_backup, 'rb') as f:
        compressed_data = f.read()

    try:
        decompressed_data = zlib.decompress(compressed_data).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to decompress {target_backup}: {e}")

    assert decompressed_data == expected_data, (
        f"Decompressed data does not match expected output.\n"
        f"Expected:\n{repr(expected_data)}\n"
        f"Got:\n{repr(decompressed_data)}"
    )
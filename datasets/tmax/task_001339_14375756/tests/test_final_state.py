# test_final_state.py

import os
import pytest

def compute_rle(data: bytes) -> bytes:
    """Computes the custom RLE for the given bytes."""
    if not data:
        return b""

    result = bytearray()
    current_byte = data[0]
    count = 1

    for b in data[1:]:
        if b == current_byte and count < 255:
            count += 1
        else:
            result.append(count)
            result.append(current_byte)
            current_byte = b
            count = 1

    result.append(count)
    result.append(current_byte)
    return bytes(result)

def get_cfg_files(base_dir: str):
    """Recursively finds all .cfg files in the base directory."""
    cfg_files = []
    for root, _, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.cfg'):
                cfg_files.append(os.path.join(root, f))
    return cfg_files

def test_snapshot_files_exist_and_correct():
    sys_config_dir = '/home/user/sys_config'
    snapshots_dir = '/home/user/snapshots'

    assert os.path.exists(sys_config_dir), f"Directory {sys_config_dir} does not exist."
    assert os.path.exists(snapshots_dir), f"Directory {snapshots_dir} does not exist."

    cfg_files = get_cfg_files(sys_config_dir)
    assert len(cfg_files) > 0, "No .cfg files found in sys_config to test."

    for cfg_path in cfg_files:
        rel_path = os.path.relpath(cfg_path, sys_config_dir)
        snapshot_path = os.path.join(snapshots_dir, f"{rel_path}.rle")

        assert os.path.exists(snapshot_path), f"Expected snapshot file missing: {snapshot_path}"

        with open(cfg_path, 'rb') as f:
            original_data = f.read()

        expected_rle_data = compute_rle(original_data)

        with open(snapshot_path, 'rb') as f:
            actual_rle_data = f.read()

        assert actual_rle_data == expected_rle_data, (
            f"RLE compressed data in {snapshot_path} is incorrect.\n"
            f"Expected {len(expected_rle_data)} bytes, got {len(actual_rle_data)} bytes."
        )

def test_ignored_files_not_processed():
    snapshots_dir = '/home/user/snapshots'
    ignore_file_rel = 'ignore.txt'

    # Check that ignore.txt wasn't processed
    snapshot_ignore_path = os.path.join(snapshots_dir, f"{ignore_file_rel}.rle")
    assert not os.path.exists(snapshot_ignore_path), f"File {ignore_file_rel} should have been ignored, but {snapshot_ignore_path} exists."

def test_no_tmp_files_left_over():
    snapshots_dir = '/home/user/snapshots'
    assert os.path.exists(snapshots_dir), f"Directory {snapshots_dir} does not exist."

    tmp_files = []
    for root, _, files in os.walk(snapshots_dir):
        for f in files:
            if f.endswith('.tmp'):
                tmp_files.append(os.path.join(root, f))

    assert len(tmp_files) == 0, f"Temporary files were left in the snapshots directory, failing the atomic write requirement: {tmp_files}"

def test_snapshot_log_correct():
    log_path = '/home/user/snapshot_log.txt'
    sys_config_dir = '/home/user/sys_config'

    assert os.path.exists(log_path), f"Log file missing: {log_path}"

    cfg_files = get_cfg_files(sys_config_dir)

    expected_log_lines = []
    for cfg_path in cfg_files:
        rel_path = os.path.relpath(cfg_path, sys_config_dir)
        with open(cfg_path, 'rb') as f:
            rle_data = compute_rle(f.read())
        expected_log_lines.append(f"{rel_path} -> {len(rle_data)} bytes")

    expected_log_lines.sort()
    expected_log_content = "\n".join(expected_log_lines)

    with open(log_path, 'r') as f:
        actual_log_content = f.read().strip()

    assert actual_log_content == expected_log_content, (
        f"Log file {log_path} content is incorrect.\n"
        f"Expected:\n{expected_log_content}\n"
        f"Got:\n{actual_log_content}"
    )
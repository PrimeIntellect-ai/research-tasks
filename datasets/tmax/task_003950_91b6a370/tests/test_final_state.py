# test_final_state.py

import os
import pytest

def test_cfg_files_created():
    """Verify that the correct .cfg files are created and the corrupted one is skipped."""
    expected_cfg_files = [
        "/home/user/configs/db/node1.cfg",
        "/home/user/configs/db/node2.cfg",
        "/home/user/configs/web/front.cfg",
    ]

    for cfg in expected_cfg_files:
        assert os.path.isfile(cfg), f"Expected file {cfg} was not created."

def test_corrupt_cfg_skipped():
    """Verify that the corrupted .bak file was not extracted."""
    corrupted_cfg = "/home/user/configs/cache/redis.cfg"
    assert not os.path.exists(corrupted_cfg), f"Corrupted file {corrupted_cfg} should not have been extracted."

def test_tracked_changes_log_exists():
    """Verify that the tracked_changes.log file was created."""
    log_file = "/home/user/tracked_changes.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

def test_tracked_changes_log_content():
    """Verify the contents of tracked_changes.log match the expected output exactly."""
    log_file = "/home/user/tracked_changes.log"

    expected_lines = [
        "front.cfg: £50_bonus_promo",
        "node1.cfg: schema_v5",
        "node2.cfg: schema_v5_replica"
    ]

    with open(log_file, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {log_file} do not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_utf8_encoding():
    """Verify that the extracted front.cfg is properly UTF-8 encoded."""
    front_cfg = "/home/user/configs/web/front.cfg"
    if os.path.exists(front_cfg):
        try:
            with open(front_cfg, "r", encoding="utf-8") as f:
                content = f.read()
            assert "£50_bonus_promo" in content, "The £ symbol was not correctly converted to UTF-8 in front.cfg."
        except UnicodeDecodeError:
            pytest.fail(f"File {front_cfg} is not properly UTF-8 encoded.")
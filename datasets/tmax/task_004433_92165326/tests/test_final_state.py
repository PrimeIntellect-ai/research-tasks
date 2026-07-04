# test_final_state.py

import os
import json
import pytest

def test_summary_json_exists_and_correct():
    summary_path = '/home/user/summary.json'
    assert os.path.isfile(summary_path), f"Summary JSON file missing at {summary_path}"

    with open(summary_path, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json is not a valid JSON file.")

    assert "bytes_saved" in summary, "Missing 'bytes_saved' in summary.json"
    assert summary["bytes_saved"] == 10, f"Expected bytes_saved to be 10, got {summary['bytes_saved']}"

    assert "hard_links_created" in summary, "Missing 'hard_links_created' in summary.json"
    assert summary["hard_links_created"] == 1, f"Expected hard_links_created to be 1, got {summary['hard_links_created']}"

    assert "symlinks_created" in summary, "Missing 'symlinks_created' in summary.json"
    assert summary["symlinks_created"] == 3, f"Expected symlinks_created to be 3, got {summary['symlinks_created']}"

def test_hard_links_created_correctly():
    f1_path = '/home/user/data_volume/f1.dat'
    f2_path = '/home/user/data_volume/f2.dat'
    f3_path = '/home/user/data_volume/f3.dat'
    f4_path = '/home/user/data_volume/f4.dat'

    assert os.path.isfile(f1_path), f"{f1_path} is missing"
    assert os.path.isfile(f2_path), f"{f2_path} is missing"
    assert os.path.isfile(f3_path), f"{f3_path} is missing"
    assert os.path.isfile(f4_path), f"{f4_path} is missing"

    stat1 = os.stat(f1_path)
    stat2 = os.stat(f2_path)

    assert stat1.st_ino == stat2.st_ino, "f1.dat and f2.dat should be hardlinked (same inode), but they are not."

    stat3 = os.stat(f3_path)
    stat4 = os.stat(f4_path)

    assert stat3.st_ino != stat4.st_ino, "f3.dat and f4.dat are ACTIVE and should NOT be hardlinked, but they have the same inode."

def test_symlinks_created_correctly():
    archive_dir = '/home/user/archive_links'
    data_dir = '/home/user/data_volume'

    expected_symlinks = ['f1.dat', 'f2.dat', 'f5.dat']
    unexpected_symlinks = ['f3.dat', 'f4.dat']

    for fname in expected_symlinks:
        symlink_path = os.path.join(archive_dir, fname)
        target_path = os.path.join(data_dir, fname)

        assert os.path.islink(symlink_path), f"Expected symlink at {symlink_path} is missing or not a symlink."

        actual_target = os.readlink(symlink_path)
        assert actual_target == target_path, f"Symlink {symlink_path} points to {actual_target}, expected {target_path}."

    for fname in unexpected_symlinks:
        symlink_path = os.path.join(archive_dir, fname)
        assert not os.path.exists(symlink_path), f"Symlink {symlink_path} should not exist because the file is ACTIVE."
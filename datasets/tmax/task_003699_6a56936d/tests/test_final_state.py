# test_final_state.py

import os
import stat
import re

def test_symlink_live_exists():
    link_path = "/home/user/docs/live"
    target_path = "/home/user/docs/published"
    assert os.path.islink(link_path), f"Expected {link_path} to be a symbolic link."
    assert os.readlink(link_path) == target_path, f"Expected {link_path} to point to {target_path}."

def test_hardlinks_exist_and_match():
    src_ch1 = "/home/user/docs/src/ch1.md"
    pub_ch1 = "/home/user/docs/published/ch1.md"

    assert os.path.isfile(src_ch1), f"Expected {src_ch1} to exist."
    assert os.path.isfile(pub_ch1), f"Expected {pub_ch1} to exist."
    assert os.stat(src_ch1).st_ino == os.stat(pub_ch1).st_ino, f"{pub_ch1} is not a hardlink to {src_ch1}."

    src_logo = "/home/user/docs/src/assets/logo.png"
    pub_logo = "/home/user/docs/published/assets/logo.png"

    assert os.path.isfile(src_logo), f"Expected {src_logo} to exist."
    assert os.path.isfile(pub_logo), f"Expected {pub_logo} to exist."
    assert os.stat(src_logo).st_ino == os.stat(pub_logo).st_ino, f"{pub_logo} is not a hardlink to {src_logo}."

def test_draft_deleted_in_published():
    pub_draft = "/home/user/docs/published/draft.md"
    assert not os.path.exists(pub_draft), f"Expected {pub_draft} to be deleted."

def test_daemon_log_exists_and_format():
    log_path = "/home/user/docs/daemon.log"
    assert os.path.isfile(log_path), f"Expected {log_path} to exist."

    with open(log_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "Expected daemon.log to have content."

    pattern = re.compile(r"^EVENT:\s+\w+\s+\|\s+PATH:\s+/.+")
    valid_lines = [line for line in lines if pattern.match(line.strip())]

    assert len(valid_lines) > 0, "Expected at least one line matching the EVENT format in daemon.log."

def test_incremental_backups_exist():
    snar_path = "/home/user/docs/backups/snapshot.snar"
    assert os.path.isfile(snar_path), f"Expected {snar_path} to exist."

    backup_0 = "/home/user/docs/backups/backup_0.tar"
    backup_1 = "/home/user/docs/backups/backup_1.tar"

    assert os.path.isfile(backup_0), f"Expected {backup_0} to exist."
    assert os.path.isfile(backup_1), f"Expected {backup_1} to exist."
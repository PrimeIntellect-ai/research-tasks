# test_final_state.py
import os

def test_corrupted_log():
    log_path = "/home/user/repo/corrupted.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()
    assert "bad_data.tar.gz" in content, f"Expected 'bad_data.tar.gz' in {log_path}, got {content}"

def test_symlinks_created():
    symlink1 = "/home/user/repo/database/sqldb/1.0.0/payload.tar.gz"
    target1 = "/home/user/incoming/db_v1.tar.gz"

    symlink2 = "/home/user/repo/web/server/2.1.4/payload.tar.gz"
    target2 = "/home/user/incoming/web_v2.tar.gz"

    assert os.path.islink(symlink1), f"{symlink1} is not a symlink."
    assert os.readlink(symlink1) == target1, f"{symlink1} does not point to {target1}."

    assert os.path.islink(symlink2), f"{symlink2} is not a symlink."
    assert os.readlink(symlink2) == target2, f"{symlink2} does not point to {target2}."

def test_final_layout_txt():
    layout_path = "/home/user/repo/final_layout.txt"
    assert os.path.exists(layout_path), f"File {layout_path} does not exist."
    with open(layout_path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "/home/user/repo/database/sqldb/1.0.0/payload.tar.gz",
        "/home/user/repo/web/server/2.1.4/payload.tar.gz"
    ]
    assert content == expected, f"Expected {layout_path} to contain exactly {expected}, got {content}"
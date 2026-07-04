# test_final_state.py

import os
import stat
import pytest

def test_curator_executable_exists():
    curator_path = "/home/user/curator"
    assert os.path.isfile(curator_path), f"Executable {curator_path} does not exist."
    st = os.stat(curator_path)
    assert st.st_mode & stat.S_IXUSR, f"Executable {curator_path} is not executable."

def test_repo_files_exist():
    expected_files = [
        "a_first.bin",
        "b_second.bin",
        "c_third.bin",
        "f_fourth.bin"
    ]
    for filename in expected_files:
        filepath = os.path.join("/home/user/artifacts_repo", filename)
        assert os.path.isfile(filepath), f"Expected file {filepath} is missing in artifacts_repo."

def test_ignored_files_do_not_exist():
    ignored_files = [
        "d_active.tmp",
        "e_text.txt"
    ]
    for filename in ignored_files:
        filepath = os.path.join("/home/user/artifacts_repo", filename)
        assert not os.path.exists(filepath), f"Ignored file {filepath} should NOT be in artifacts_repo."

def test_hard_links():
    repo_dir = "/home/user/artifacts_repo"

    a_first = os.path.join(repo_dir, "a_first.bin")
    c_third = os.path.join(repo_dir, "c_third.bin")
    b_second = os.path.join(repo_dir, "b_second.bin")
    f_fourth = os.path.join(repo_dir, "f_fourth.bin")

    # Check existence to avoid stat errors
    assert os.path.exists(a_first) and os.path.exists(c_third), "Missing files for hardlink check (a_first, c_third)"
    assert os.path.exists(b_second) and os.path.exists(f_fourth), "Missing files for hardlink check (b_second, f_fourth)"

    stat_a = os.stat(a_first)
    stat_c = os.stat(c_third)

    assert stat_a.st_nlink >= 2, f"{a_first} does not have multiple hard links."
    assert stat_a.st_ino == stat_c.st_ino, f"{a_first} and {c_third} are not hard linked."

    stat_b = os.stat(b_second)
    stat_f = os.stat(f_fourth)

    assert stat_b.st_nlink >= 2, f"{b_second} does not have multiple hard links."
    assert stat_b.st_ino == stat_f.st_ino, f"{b_second} and {f_fourth} are not hard linked."

def test_latest_symlink():
    symlink_path = "/home/user/artifacts_repo/latest.elf"
    assert os.path.islink(symlink_path), f"{symlink_path} does not exist or is not a symlink."

    target = os.readlink(symlink_path)
    # Target can be absolute or relative
    if not os.path.isabs(target):
        target = os.path.join("/home/user/artifacts_repo", target)

    target_norm = os.path.normpath(target)
    expected_target = "/home/user/artifacts_repo/f_fourth.bin"

    assert target_norm == expected_target, f"latest.elf symlink points to {target_norm}, expected {expected_target}."
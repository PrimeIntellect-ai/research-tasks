# test_final_state.py

import os
import pytest

def test_symlink_sanitization():
    curated_repo = "/home/user/curated_repo"
    bad_symlink = os.path.join(curated_repo, "system_passwords")
    good_symlink = os.path.join(curated_repo, "info.txt")

    assert not os.path.exists(bad_symlink) and not os.path.islink(bad_symlink), \
        f"Malicious symlink {bad_symlink} should have been deleted."

    assert os.path.islink(good_symlink), \
        f"Valid symlink {good_symlink} should still exist."

def test_utf8_conversion():
    readme_path = "/home/user/curated_repo/readme.txt"
    assert os.path.exists(readme_path), f"{readme_path} is missing."

    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        pytest.fail(f"{readme_path} is not valid UTF-8.")

    assert "über fast execution" in content, \
        f"Expected converted text not found in {readme_path}. Found: {content}"

def test_file_renaming():
    curated_repo = "/home/user/curated_repo"
    expected_files = ["core_system_app.elf", "diagnostic_tool.elf"]
    unexpected_files = ["core system app.bin", "diagnostic tool.bin"]

    for f in expected_files:
        path = os.path.join(curated_repo, f)
        assert os.path.exists(path), f"Expected renamed file {path} is missing."

    for f in unexpected_files:
        path = os.path.join(curated_repo, f)
        assert not os.path.exists(path), f"Old file {path} should not exist."

def test_hard_links():
    curated_repo = "/home/user/curated_repo"
    release_dir = os.path.join(curated_repo, "release")

    assert os.path.isdir(release_dir), f"{release_dir} directory is missing."

    files_to_check = ["core_system_app.elf", "diagnostic_tool.elf"]
    for f in files_to_check:
        orig_path = os.path.join(curated_repo, f)
        link_path = os.path.join(release_dir, f)

        assert os.path.exists(link_path), f"Hard link {link_path} is missing."

        orig_stat = os.stat(orig_path)
        link_stat = os.stat(link_path)

        assert orig_stat.st_ino == link_stat.st_ino, \
            f"{link_path} is not a hard link to {orig_path} (inodes differ)."

def test_latest_symlink():
    symlink_path = "/home/user/curated_repo/latest"
    expected_target_name = "release"
    expected_target_abs = "/home/user/curated_repo/release"

    assert os.path.islink(symlink_path), f"{symlink_path} should be a symbolic link."

    target = os.readlink(symlink_path)
    assert target in (expected_target_name, expected_target_abs), \
        f"Symlink {symlink_path} points to {target}, expected {expected_target_name} or {expected_target_abs}."

def test_audit_log():
    log_path = "/home/user/audit.log"
    assert os.path.exists(log_path), f"Audit log {log_path} is missing."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["core_system_app.elf", "diagnostic_tool.elf"]
    assert lines == expected_lines, \
        f"Audit log contents incorrect. Expected {expected_lines}, got {lines}."
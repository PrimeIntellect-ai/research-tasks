# test_final_state.py

import os
import tarfile
import pytest

def test_skipped_links_file():
    skipped_links_path = "/home/user/skipped_links.txt"
    assert os.path.exists(skipped_links_path), f"File {skipped_links_path} does not exist."

    with open(skipped_links_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_links = [
        "/home/user/configs/app_beta/loop1.lnk",
        "/home/user/configs/app_beta/loop2.lnk",
        "/home/user/configs/app_gamma/self_loop.lnk"
    ]

    assert lines == expected_links, f"Expected skipped links {expected_links}, but got {lines}."

def test_app_beta_archive():
    archive_path = "/home/user/archives/app_beta.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()
        # Extract base names of members, ignoring directory entries if any
        file_names = {os.path.basename(m.name) for m in members if m.isfile()}

        assert "config.ini" in file_names, "config.ini missing from app_beta.tar.gz"
        assert "valid_link.ini" in file_names, "valid_link.ini missing from app_beta.tar.gz"
        assert "loop1.lnk" not in file_names, "loop1.lnk should not be in app_beta.tar.gz"
        assert "loop2.lnk" not in file_names, "loop2.lnk should not be in app_beta.tar.gz"

        # Verify valid_link.ini was dereferenced and contains the correct data
        valid_link_member = next(m for m in members if os.path.basename(m.name) == "valid_link.ini")
        assert valid_link_member.isfile(), "valid_link.ini must be stored as a regular file, not a symlink."

        f = tar.extractfile(valid_link_member)
        content = f.read().decode('utf-8').strip()
        assert content == "beta_setting=2", f"valid_link.ini content incorrect: {content}"

def test_app_gamma_archive():
    archive_path = "/home/user/archives/app_gamma.tar.gz"
    assert os.path.exists(archive_path), f"Archive {archive_path} does not exist."

    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()
        file_names = {os.path.basename(m.name) for m in members if m.isfile()}

        assert "settings.conf" in file_names, "settings.conf missing from app_gamma.tar.gz"
        assert "cross_link.ini" in file_names, "cross_link.ini missing from app_gamma.tar.gz"
        assert "self_loop.lnk" not in file_names, "self_loop.lnk should not be in app_gamma.tar.gz"

        cross_link_member = next(m for m in members if os.path.basename(m.name) == "cross_link.ini")
        assert cross_link_member.isfile(), "cross_link.ini must be stored as a regular file, not a symlink."

        f = tar.extractfile(cross_link_member)
        content = f.read().decode('utf-8').strip()
        assert content == "beta_setting=2", f"cross_link.ini content incorrect: {content}"

def test_fcntl_used():
    script_path = "/home/user/archive_configs.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "fcntl" in content, "The script must use fcntl for file locking as requested."
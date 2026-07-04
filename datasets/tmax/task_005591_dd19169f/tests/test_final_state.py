# test_final_state.py
import os
import stat
import pytest

def test_parser_c_exists_and_uses_mmap():
    """Verify that parser.c exists and contains 'mmap'."""
    parser_path = "/home/user/parser.c"
    assert os.path.isfile(parser_path), f"C parser source file {parser_path} is missing."

    with open(parser_path, "r") as f:
        content = f.read()

    assert "mmap" in content, "The C parser must use mmap as per the requirements."

def test_fatal_errors_hard_links():
    """Verify that FATAL errors resulted in correct hard links."""
    expected_links = {
        "/home/user/fatal_errors/main.c": "/home/user/src/app/main.c",
        "/home/user/fatal_errors/socket.c": "/home/user/src/network/socket.c",
    }

    for link_path, target_path in expected_links.items():
        assert os.path.exists(link_path), f"Hard link {link_path} is missing."
        assert os.path.exists(target_path), f"Target file {target_path} is missing."

        link_stat = os.stat(link_path)
        target_stat = os.stat(target_path)

        assert link_stat.st_ino == target_stat.st_ino, f"{link_path} is not a hard link to {target_path}."
        assert not os.path.islink(link_path), f"{link_path} should be a hard link, not a symbolic link."

def test_warn_errors_symlinks():
    """Verify that WARN errors resulted in correct symbolic links."""
    expected_links = {
        "/home/user/warn_errors/math.c": "/home/user/src/lib/math.c",
        "/home/user/warn_errors/missing.c": "/home/user/src/app/missing.c",
    }

    for link_path, target_path in expected_links.items():
        assert os.path.islink(link_path), f"{link_path} is missing or is not a symbolic link."

        actual_target = os.readlink(link_path)
        assert actual_target == target_path, f"Symlink {link_path} points to {actual_target}, expected {target_path}."
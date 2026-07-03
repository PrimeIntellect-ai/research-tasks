# test_final_state.py

import os
import pytest

def test_source_file_exists():
    source_path = "/home/user/bin/healthcheck.c"
    assert os.path.isfile(source_path), f"Source file {source_path} is missing."

def test_executable_exists_and_executable():
    executable_path = "/home/user/bin/healthcheck"
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_active_symlinks_retained():
    retained_links = ["srv1", "srv3"]
    for link_name in retained_links:
        link_path = f"/home/user/pool/{link_name}"
        assert os.path.islink(link_path), f"Symlink {link_path} should exist because its port is open."

def test_dead_symlinks_removed():
    removed_links = ["srv2", "srv4"]
    for link_name in removed_links:
        link_path = f"/home/user/pool/{link_name}"
        assert not os.path.exists(link_path), f"Symlink {link_path} should have been removed because its port is closed."
        assert not os.path.islink(link_path), f"Symlink {link_path} should have been removed because its port is closed."
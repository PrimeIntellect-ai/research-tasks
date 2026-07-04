# test_final_state.py

import os
import re
import pytest

def test_binaries_exist_and_format():
    linux_bin = "/home/user/webapp/build/server_linux"
    windows_bin = "/home/user/webapp/build/server_windows.exe"

    assert os.path.isfile(linux_bin), f"Linux binary not found at {linux_bin}"
    assert os.path.isfile(windows_bin), f"Windows binary not found at {windows_bin}"

    # Check magic bytes for ELF (Linux)
    with open(linux_bin, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{linux_bin} is not a valid ELF executable"

    # Check magic bytes for PE (Windows)
    with open(windows_bin, "rb") as f:
        magic = f.read(2)
        assert magic == b"MZ", f"{windows_bin} is not a valid PE executable"

def test_windows_build_tags():
    proc_windows_path = "/home/user/webapp/proc_windows.go"
    assert os.path.isfile(proc_windows_path), f"File {proc_windows_path} is missing."

    with open(proc_windows_path, "r") as f:
        content = f.read()

    has_new_tag = "go:build windows" in content
    has_old_tag = "+build windows" in content

    assert has_new_tag or has_old_tag, f"Missing Windows build tag in {proc_windows_path}"

def test_memory_leak_fixed():
    thumbnail_path = "/home/user/webapp/thumbnail.go"
    assert os.path.isfile(thumbnail_path), f"File {thumbnail_path} is missing."

    with open(thumbnail_path, "r") as f:
        content = f.read()

    assert "LeakCache = append" not in content, f"Memory leak is not fixed in {thumbnail_path}"

def test_patch_applied():
    main_go_path = "/home/user/webapp/main.go"
    assert os.path.isfile(main_go_path), f"File {main_go_path} is missing."

    with open(main_go_path, "r") as f:
        content = f.read()

    assert "HandleThumbnail" in content, f"Patch was not properly applied to {main_go_path}"
    assert "PATCH_INSERT_ROUTE" not in content, f"Patch was not properly applied to {main_go_path}"
# test_final_state.py

import os
import pytest

def test_manifest_log_contents():
    manifest_path = "/home/user/release/manifest.log"
    assert os.path.isfile(manifest_path), f"File missing: {manifest_path}"

    with open(manifest_path, "r") as f:
        content = f.read().strip()

    expected = "58 10 213 26"
    assert content == expected, f"Incorrect manifest.log content. Expected '{expected}', got '{content}'"

def test_makefile_fixed():
    makefile_path = "/home/user/release/libemu/Makefile"
    assert os.path.isfile(makefile_path), f"File missing: {makefile_path}"

    with open(makefile_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "ar rcs" in line or "$(CC)" in line:
            assert line.startswith("\t"), f"Makefile line {i+1} does not start with a tab: {repr(line)}"

def test_libemu_compiled():
    libemu_path = "/home/user/release/libemu/libemu.a"
    assert os.path.isfile(libemu_path), f"Compiled library missing: {libemu_path}"

def test_main_go_fixed():
    main_go_path = "/home/user/release/go-emu/main.go"
    assert os.path.isfile(main_go_path), f"File missing: {main_go_path}"

    with open(main_go_path, "r") as f:
        content = f.read()

    # Check that state = STATE_ESCAPED is present and not commented out
    lines = content.split('\n')
    found_transition = False
    in_ee_block = False

    for line in lines:
        if "b == 0xEE" in line:
            in_ee_block = True
        elif in_ee_block and "else" in line:
            in_ee_block = False

        if in_ee_block:
            stripped = line.strip()
            if stripped.startswith("state") and "STATE_ESCAPED" in stripped and not stripped.startswith("//"):
                found_transition = True
                break

    assert found_transition, "main.go does not correctly transition to STATE_ESCAPED when b == 0xEE"
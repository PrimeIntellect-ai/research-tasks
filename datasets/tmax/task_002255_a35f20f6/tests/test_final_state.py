# test_final_state.py

import os
import pytest

def test_utf8_files_created_and_content():
    omega_path = "/home/user/organized/utf8/OMEGA-77.txt"
    delta_path = "/home/user/organized/utf8/DELTA-04.txt"

    assert os.path.isfile(omega_path), f"Missing UTF-8 file: {omega_path}"
    assert os.path.isfile(delta_path), f"Missing UTF-8 file: {delta_path}"

    with open(omega_path, "r", encoding="utf-8") as f:
        omega_content = f.read()
    assert "ProjectID: OMEGA-77" in omega_content, f"Incorrect content in {omega_path}"

    with open(delta_path, "r", encoding="utf-8") as f:
        delta_content = f.read()
    assert "ProjectID: DELTA-04" in delta_content, f"Incorrect content in {delta_path}"

def test_hard_links_created():
    omega_bak = "/home/user/organized/archive/OMEGA-77_raw.bak"
    delta_bak = "/home/user/organized/archive/DELTA-04_raw.bak"

    dataset_a = "/home/user/incoming/dataset_a.csv"
    dataset_b = "/home/user/incoming/dataset_b.dat"

    assert os.path.isfile(omega_bak), f"Missing hard link: {omega_bak}"
    assert os.path.isfile(delta_bak), f"Missing hard link: {delta_bak}"

    assert os.stat(omega_bak).st_ino == os.stat(dataset_a).st_ino, f"{omega_bak} is not a hard link to {dataset_a}"
    assert os.stat(delta_bak).st_ino == os.stat(dataset_b).st_ino, f"{delta_bak} is not a hard link to {dataset_b}"

def test_symlinks_created():
    omega_symlink = "/home/user/organized/symlinks/OMEGA-77_active"
    delta_symlink = "/home/user/organized/symlinks/DELTA-04_active"

    omega_target = "/home/user/organized/utf8/OMEGA-77.txt"
    delta_target = "/home/user/organized/utf8/DELTA-04.txt"

    assert os.path.islink(omega_symlink), f"Missing symlink: {omega_symlink}"
    assert os.path.islink(delta_symlink), f"Missing symlink: {delta_symlink}"

    assert os.readlink(omega_symlink) == omega_target, f"{omega_symlink} points to incorrect target"
    assert os.readlink(delta_symlink) == delta_target, f"{delta_symlink} points to incorrect target"
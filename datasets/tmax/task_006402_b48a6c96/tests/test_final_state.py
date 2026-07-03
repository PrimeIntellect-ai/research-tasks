# test_final_state.py

import os
import subprocess
import pytest

def get_build_id(filepath):
    """Helper to extract the GNU Build ID using readelf."""
    try:
        output = subprocess.check_output(['readelf', '-n', filepath], universal_newlines=True)
        for line in output.splitlines():
            if "Build ID" in line:
                return line.split()[-1].strip()
    except Exception as e:
        pytest.fail(f"Failed to extract Build ID from {filepath}: {e}")
    return None

def test_directories_extracted():
    assert os.path.isdir("/home/user/extracted/app_v1"), "app_v1 was not extracted"
    assert os.path.isdir("/home/user/extracted/app_v2"), "app_v2 was not extracted"
    assert not os.path.isdir("/home/user/extracted/app_v3"), "app_v3 should have been skipped due to corruption"
    assert os.path.isdir("/home/user/extracted/app_v4"), "app_v4 was not extracted"

def test_log_symlinks():
    link_v1 = "/home/user/log_links/app_v1_backup.log"
    link_v2 = "/home/user/log_links/app_v2_backup.log"
    link_v4 = "/home/user/log_links/app_v4_backup.log"

    assert os.path.islink(link_v1), f"{link_v1} is missing or not a symlink"
    assert os.path.islink(link_v2), f"{link_v2} is missing or not a symlink"
    assert not os.path.islink(link_v4), f"{link_v4} should not exist (FAILED status)"

    # Verify targets
    target_v1 = os.readlink(link_v1)
    target_v2 = os.readlink(link_v2)

    assert target_v1 == "/home/user/extracted/app_v1/app_v1/backup.log", f"Symlink target for v1 is incorrect: {target_v1}"
    assert target_v2 == "/home/user/extracted/app_v2/app_v2/backup.log", f"Symlink target for v2 is incorrect: {target_v2}"

def test_elf_deduplication():
    id_ls = get_build_id("/bin/ls")
    id_cat = get_build_id("/bin/cat")
    id_echo = get_build_id("/bin/echo")

    assert id_ls, "Could not get Build ID for /bin/ls"
    assert id_cat, "Could not get Build ID for /bin/cat"
    assert id_echo, "Could not get Build ID for /bin/echo"

    master_ls = f"/home/user/elf_master/{id_ls}.elf"
    master_cat = f"/home/user/elf_master/{id_cat}.elf"
    master_echo = f"/home/user/elf_master/{id_echo}.elf"

    assert os.path.isfile(master_ls), f"Master ELF for ls ({master_ls}) is missing"
    assert os.path.isfile(master_cat), f"Master ELF for cat ({master_cat}) is missing"
    assert os.path.isfile(master_echo), f"Master ELF for echo ({master_echo}) is missing"

    inode_master_ls = os.stat(master_ls).st_ino
    inode_v1_app = os.stat("/home/user/extracted/app_v1/app_v1/bin/app").st_ino
    inode_v2_app = os.stat("/home/user/extracted/app_v2/app_v2/bin/app").st_ino

    assert inode_master_ls == inode_v1_app, "Hardlink for app_v1 bin/app (ls) does not match master"
    assert inode_master_ls == inode_v2_app, "Hardlink for app_v2 bin/app (ls) does not match master"

    inode_master_cat = os.stat(master_cat).st_ino
    inode_v1_cat = os.stat("/home/user/extracted/app_v1/app_v1/bin/helper").st_ino

    assert inode_master_cat == inode_v1_cat, "Hardlink for app_v1 bin/helper (cat) does not match master"

    inode_v4_app = os.stat("/home/user/extracted/app_v4/app_v4/bin/app").st_ino
    assert inode_master_cat != inode_v4_app, "Failed backup (app_v4) was incorrectly deduplicated"
# test_final_state.py

import os
import pytest
import tarfile

def test_x86_64_binaries_exist():
    """Check that x86_64 binaries exist."""
    path_1_0_5 = '/home/user/repo/x86_64/server_bin-1.0.5.elf'
    path_1_2_0 = '/home/user/repo/x86_64/server_bin-1.2.0.elf'
    assert os.path.isfile(path_1_0_5), f"Expected file {path_1_0_5} does not exist."
    assert os.path.isfile(path_1_2_0), f"Expected file {path_1_2_0} does not exist."

def test_aarch64_binaries_exist():
    """Check that aarch64 binaries exist."""
    path_client = '/home/user/repo/aarch64/client_bin-2.1.0.elf'
    path_proxy = '/home/user/repo/aarch64/proxy_bin-3.0.0.elf'
    assert os.path.isfile(path_client), f"Expected file {path_client} does not exist."
    assert os.path.isfile(path_proxy), f"Expected file {path_proxy} does not exist."

def test_failed_binary_not_in_repo():
    """Check that worker_bin is not in the repo."""
    for root, dirs, files in os.walk('/home/user/repo'):
        for file in files:
            assert 'worker_bin' not in file, f"Failed binary worker_bin found in repo: {os.path.join(root, file)}"

def test_symlink_latest():
    """Check that server_bin-latest.elf is a symlink to server_bin-1.2.0.elf."""
    symlink_path = '/home/user/repo/x86_64/server_bin-latest.elf'
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    target = os.readlink(symlink_path)
    # The target might be absolute or relative, but it should resolve to server_bin-1.2.0.elf
    assert 'server_bin-1.2.0.elf' in target, f"Symlink {symlink_path} does not point to server_bin-1.2.0.elf, points to {target}"

def test_hardlink_all_binaries():
    """Check that files in all_binaries are hardlinks to the arch folders."""
    arch_file = '/home/user/repo/x86_64/server_bin-1.2.0.elf'
    all_bin_file = '/home/user/repo/all_binaries/server_bin-1.2.0.elf'

    assert os.path.isfile(arch_file), f"Missing {arch_file}"
    assert os.path.isfile(all_bin_file), f"Missing {all_bin_file}"

    stat_arch = os.stat(arch_file)
    stat_all = os.stat(all_bin_file)

    assert stat_arch.st_ino == stat_all.st_ino, f"{all_bin_file} is not a hardlink to {arch_file} (inodes differ)"

def test_final_archive_exists():
    """Check that the final tarball exists and is a valid tar file."""
    archive_path = '/home/user/repo_curated.tar.gz'
    assert os.path.isfile(archive_path), f"Final archive {archive_path} does not exist."
    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."
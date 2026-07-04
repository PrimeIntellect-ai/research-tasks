# test_final_state.py

import os
import tarfile
import pytest

def test_workspace_extracted():
    workspace_dir = "/home/user/workspace/messy"
    assert os.path.isdir(workspace_dir), f"Expected extracted directory {workspace_dir} to exist."
    assert os.path.isfile(os.path.join(workspace_dir, "dir1/alpha.dat")), "alpha.dat missing in workspace."
    assert os.path.isfile(os.path.join(workspace_dir, "dir3/delta.dat")), "delta.dat missing in workspace."
    assert os.path.isfile(os.path.join(workspace_dir, "logs/run2.log")), "run2.log missing in workspace."

def test_organized_dataset_hardlinks():
    data_dir = "/home/user/organized_dataset/data"
    assert os.path.isdir(data_dir), f"Directory {data_dir} does not exist."

    sub1 = os.path.join(data_dir, "subject_001.dat")
    sub2 = os.path.join(data_dir, "subject_002.dat")

    assert os.path.isfile(sub1), f"File {sub1} does not exist."
    assert os.path.isfile(sub2), f"File {sub2} does not exist."

    # Check sizes
    assert os.path.getsize(sub1) == 15000, f"{sub1} has incorrect size. Expected 15000 bytes."
    assert os.path.getsize(sub2) == 12000, f"{sub2} has incorrect size. Expected 12000 bytes."

    # Check hard links
    alpha_path = "/home/user/workspace/messy/dir1/alpha.dat"
    delta_path = "/home/user/workspace/messy/dir3/delta.dat"

    assert os.path.exists(alpha_path), f"{alpha_path} does not exist."
    assert os.path.exists(delta_path), f"{delta_path} does not exist."

    stat_sub1 = os.stat(sub1)
    stat_alpha = os.stat(alpha_path)
    assert stat_sub1.st_ino == stat_alpha.st_ino, f"{sub1} is not a hard link to {alpha_path}."

    stat_sub2 = os.stat(sub2)
    stat_delta = os.stat(delta_path)
    assert stat_sub2.st_ino == stat_delta.st_ino, f"{sub2} is not a hard link to {delta_path}."

def test_organized_dataset_symlink():
    symlink_path = "/home/user/organized_dataset/latest_run.log"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    # The target might be absolute or relative, but it must resolve to run2.log
    resolved_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    expected_target = "/home/user/workspace/messy/logs/run2.log"

    assert resolved_target == expected_target, f"Symlink points to {resolved_target}, expected {expected_target}."

def test_clean_dataset_archive():
    archive_path = "/home/user/clean_dataset.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    with tarfile.open(archive_path, "r:gz") as tar:
        names = tar.getnames()

        # Check that organized_dataset is at the root of the archive
        assert any(name == "organized_dataset" or name.startswith("organized_dataset/") for name in names), \
            "Archive does not contain 'organized_dataset' at its root."

        # Check specific files exist in the archive
        expected_files = [
            "organized_dataset/data/subject_001.dat",
            "organized_dataset/data/subject_002.dat",
            "organized_dataset/latest_run.log"
        ]

        for ef in expected_files:
            assert any(name.endswith(ef) for name in names), f"Expected file {ef} missing in archive."
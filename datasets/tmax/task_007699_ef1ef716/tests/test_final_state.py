# test_final_state.py

import os
import tarfile
import pytest

def test_curate_script_exists_and_uses_flock():
    script_path = "/home/user/curate.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "fcntl.flock" in content, "The script does not appear to use fcntl.flock as requested."

def test_metadata_files_updated():
    artifacts_dir = "/home/user/artifacts"

    # Check art1.meta
    with open(os.path.join(artifacts_dir, "art1.meta"), "r") as f:
        art1_content = f.read()
    assert "status: curated" in art1_content, "art1.meta was not updated correctly."
    assert "status: pending" not in art1_content, "art1.meta still has status: pending."

    # Check art4.meta
    with open(os.path.join(artifacts_dir, "art4.meta"), "r") as f:
        art4_content = f.read()
    assert "status: curated" in art4_content, "art4.meta was not updated correctly."
    assert "status: pending" not in art4_content, "art4.meta still has status: pending."

def test_metadata_files_untouched():
    artifacts_dir = "/home/user/artifacts"

    # Check art2.meta
    with open(os.path.join(artifacts_dir, "art2.meta"), "r") as f:
        art2_content = f.read()
    assert "status: pending" in art2_content, "art2.meta should not have been updated."

    # Check art3.meta
    with open(os.path.join(artifacts_dir, "art3.meta"), "r") as f:
        art3_content = f.read()
    assert "status: curated" in art3_content, "art3.meta should remain curated."

def test_incremental_backup():
    backup_path = "/home/user/backup_inc.tar"
    assert os.path.isfile(backup_path), f"Incremental backup {backup_path} does not exist."

    with tarfile.open(backup_path, "r") as tar:
        names = tar.getnames()

        # Check that modified files are included
        assert any("art1.meta" in name for name in names), "art1.meta is missing from the incremental backup."
        assert any("art4.meta" in name for name in names), "art4.meta is missing from the incremental backup."

        # Check that unmodified files and binaries are NOT included
        assert not any("art2.meta" in name for name in names), "art2.meta should not be in the incremental backup."
        assert not any("art3.meta" in name for name in names), "art3.meta should not be in the incremental backup."
        assert not any(name.endswith(".bin") for name in names), "Binary files should not be in the incremental backup."
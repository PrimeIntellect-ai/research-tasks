# test_final_state.py
import os
import tarfile
import pytest

def test_archive_exists():
    """Verify that the archive was created."""
    tar_path = "/home/user/archives/test_run.tar.gz"
    assert os.path.exists(tar_path), f"Archive {tar_path} was not found."
    assert os.path.isfile(tar_path), f"{tar_path} is not a file."

def test_trigger_file_deleted():
    """Verify that the trigger CSV file was deleted."""
    csv_path = "/home/user/requests/test_run.csv"
    assert not os.path.exists(csv_path), f"Trigger file {csv_path} was not deleted."

def test_archive_contents():
    """Verify that the archive contains the correct files based on size metadata."""
    tar_path = "/home/user/archives/test_run.tar.gz"
    assert os.path.exists(tar_path), f"Archive {tar_path} was not found."

    expected_files = {
        "home/user/data/logs/medium.log",
        "home/user/data/logs/large.log",
        "home/user/data/backups/new.bak"
    }
    unexpected_files = {
        "home/user/data/logs/small.log",
        "home/user/data/backups/old.bak"
    }

    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            # Tarfiles might store paths with or without leading slash
            members = [m.name.lstrip('/') for m in tar.getmembers() if m.isfile()]
    except Exception as e:
        pytest.fail(f"Could not read tar file {tar_path}: {e}")

    for ef in expected_files:
        assert ef in members, f"Expected file {ef} is missing from the archive."

    for uf in unexpected_files:
        assert uf not in members, f"Unexpected file {uf} was found in the archive."
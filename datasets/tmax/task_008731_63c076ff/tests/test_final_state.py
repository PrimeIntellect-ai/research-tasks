# test_final_state.py
import os
import tarfile
import pytest

def test_docs_incoming_empty():
    incoming_dir = "/home/user/docs_incoming"
    assert os.path.isdir(incoming_dir), f"Directory {incoming_dir} does not exist"
    files = os.listdir(incoming_dir)
    assert len(files) == 0, f"Directory {incoming_dir} is not empty, found: {files}"

def test_docs_processed_files():
    processed_dir = "/home/user/docs_processed"
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} does not exist"

    processed_files = set(os.listdir(processed_dir))
    expected_files = {'lovelace_1001.json', 'turing_1002.xml', 'hopper_1003.json'}

    assert processed_files == expected_files, f"Expected files {expected_files} in {processed_dir}, but found {processed_files}"

def test_backup_files_exist():
    backup_tar = "/home/user/docs_backup/backup_1.tar"
    snapshot_snar = "/home/user/docs_backup/snapshot.snar"

    assert os.path.isfile(backup_tar), f"Backup tarball {backup_tar} is missing"
    assert os.path.isfile(snapshot_snar), f"Snapshot file {snapshot_snar} is missing"

def test_tar_contents():
    backup_tar = "/home/user/docs_backup/backup_1.tar"
    assert os.path.isfile(backup_tar), f"Backup tarball {backup_tar} is missing"

    expected_files = {'lovelace_1001.json', 'turing_1002.xml', 'hopper_1003.json'}

    try:
        with tarfile.open(backup_tar, 'r') as tar:
            tar_names = tar.getnames()
            for expected in expected_files:
                assert any(expected in name for name in tar_names), f"File {expected} is missing from the tarball {backup_tar}"
    except tarfile.ReadError:
        pytest.fail(f"File {backup_tar} is not a valid tar archive")
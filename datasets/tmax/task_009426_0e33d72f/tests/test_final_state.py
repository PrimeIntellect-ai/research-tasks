# test_final_state.py

import os
import tarfile
import pytest

def test_status_file():
    status_path = '/home/user/status.txt'
    assert os.path.isfile(status_path), f"{status_path} does not exist."
    with open(status_path, 'r') as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"Expected status.txt to contain 'SUCCESS', got '{content}'."

def test_dataset_archive_dir():
    archive_dir = '/home/user/dataset_archive'
    assert os.path.isdir(archive_dir), f"{archive_dir} does not exist."

    for i in range(1, 6):
        chunk_file = os.path.join(archive_dir, f'chunk_{i}.tar.gz')
        assert os.path.isfile(chunk_file), f"{chunk_file} does not exist."

def test_latest_symlink():
    symlink_path = '/home/user/dataset_archive/latest.tar.gz'
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    # The target could be absolute or relative, but it must resolve to chunk_5.tar.gz
    resolved_target = os.path.basename(target)
    assert resolved_target == 'chunk_5.tar.gz', f"Expected symlink to point to chunk_5.tar.gz, but points to {target}"

def test_chunk_contents():
    archive_dir = '/home/user/dataset_archive'
    for i in range(1, 6):
        chunk_file = os.path.join(archive_dir, f'chunk_{i}.tar.gz')
        assert os.path.isfile(chunk_file), f"{chunk_file} is missing."

        with tarfile.open(chunk_file, 'r:gz') as tar:
            members = tar.getnames()
            expected_txt = f'chunk_{i}.txt'
            # Allow the file to be in a subdirectory or root, but basename must match
            found = [m for m in members if os.path.basename(m) == expected_txt]
            assert found, f"{expected_txt} not found in {chunk_file}"

            member_name = found[0]
            with tar.extractfile(member_name) as f:
                lines = f.readlines()
                assert len(lines) == 10000, f"Expected 10000 lines in {expected_txt}, got {len(lines)}"

                # Check first and last line of chunk 1 as a sanity check
                if i == 1:
                    first_line = lines[0].decode('utf-8').strip()
                    last_line = lines[-1].decode('utf-8').strip()
                    assert first_line == "2023-10-25T10:00:00Z,SENSOR_1,1.5", f"Unexpected first line: {first_line}"
                    assert last_line == "2023-10-25T10:00:00Z,SENSOR_0,15000.0", f"Unexpected last line: {last_line}"

def test_final_merged_tar():
    merged_tar_path = '/home/user/final_merged.tar'
    assert os.path.isfile(merged_tar_path), f"{merged_tar_path} does not exist."

    with tarfile.open(merged_tar_path, 'r') as tar:
        members = tar.getnames()
        basenames = [os.path.basename(m) for m in members]
        for i in range(1, 6):
            expected_chunk = f'chunk_{i}.tar.gz'
            assert expected_chunk in basenames, f"{expected_chunk} not found in {merged_tar_path}"